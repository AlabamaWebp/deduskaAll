import os
import datetime

from fastapi import HTTPException, File

import sqlalchemy as sa
from sqlalchemy import select, or_, and_, func
from sqlalchemy.engine import LegacyRow

from ..schemas.agent import AgentGet
from .base import Agent, AgentType, Product, ProductType, ProductSale, engine
from ...settings import directory, time_offset

def get_AgentBase_from_list(agent: list) -> AgentGet:
    if agent == None:
        return None
    return AgentGet(
            ag_id = agent[0],
            ag_title = agent[1],
            ag_priority = agent[2],
            ag_type = agent[3],
            ag_address = agent[4],
            ag_director = agent[5],
            ag_email = agent[6],
            ag_phone = agent[7],
            ag_inn = agent[8],
            ag_kpp = agent[9],
            ag_sales = agent[10],
            ag_disc = agent[11],
            ag_image_byte = get_file_from_db(agent[12])
        )


def recount_discount(annualsales: int):
        match annualsales:
            case _ if annualsales <= 10000:
                return 0
            case _ if 10000 < annualsales <= 50000:
                return 5
            case _ if  50000 < annualsales <= 10000:
                return 10
            case _ if 150000 < annualsales <= 500000:
                return 20
            case _ if 500000 > annualsales:
                return 25


def get_agent_types() -> dict():
    query = select(AgentType.c.ID, AgentType.c.Title)
    values = engine.execute(query).fetchall()
    return values


def get_agent_type_id_by_name(type_name: str) -> int:
    query = select(AgentType.c.ID).where(AgentType.c.Title == type_name)
    value = engine.execute(query).fetchone()
    if value == None:
        return None
    return value[0]


def get_last_agent_id() -> int:
    query = select(sa.func.max(Agent.c.ID))
    value = engine.execute(query).fetchone()[0]
    if value == None:
        return 1
    return value


def get_sales_for_agent(ag_id: int) -> int:
    query = select(ProductSale).where(ProductSale.c.AgentID == ag_id)
    sales = engine.execute(query).fetchall()
    return sales


def get_agent_by_id(ag_id: int):
    query = select(
            Agent.c.ID,
            Agent.c.Title,
            Agent.c.Priority,
            select(AgentType.c.Title).where(
                    Agent.c.AgentTypeID == AgentType.c.ID
                ).label("AgentType"),
            Agent.c.Address,
            Agent.c.DirectorName,
            Agent.c.Email,
            Agent.c.Phone,
            Agent.c.INN,
            Agent.c.KPP,
            select(func.isnull(func.count(ProductSale.c.ProductCount), 0)).where(
                    and_(
                        (Agent.c.ID == ProductSale.c.AgentID),
                        (func.datediff(sa.text("yy"),
                            ProductSale.c.SaleDate,
                            func.current_date()
                        ) <= time_offset)
                    )
                ).label("AnnualSales"),
            select(func.isnull(func.sum(ProductSale.c.ProductCount * Product.c.MinCostForAgent), 0)).where(
                    and_(
                        (Agent.c.ID == ProductSale.c.AgentID),
                        (Product.c.ID == ProductSale.c.ProductID),
                        (func.datediff(sa.text("yy"),
                            ProductSale.c.SaleDate,
                            func.current_date()
                        ) <= time_offset)
                    )
                ).label("AnnualSalesBy"),
            Agent.c.Logo,
            ).where(Agent.c.ID == ag_id)
    agent = engine.execute(query).fetchone()
    return get_AgentBase_from_list(agent)


def get_pages_count(filters: dict) -> int:
    type_ = filters["ag_type"]
    search_ = f"%{filters['search']}%"
    
    query = select(sa.func.count(Agent.c.ID).label("Total")).where(
            or_(
                (Agent.c.Title.like(search_)), 
                (Agent.c.Phone.like(search_)),
                (Agent.c.Email.like(search_)),
            )
        )

    if type_ != "0":
        type_ = get_agent_type_id_by_name(type_)
        if type_ == None:
            return HTTPException(
                status_code=400,
                detail="Invalid Value",
                headers={"Invalid value": "Name of type is not in database"},
            )
        query = query.where(Agent.c.AgentTypeID == type_)

    agents_count = engine.execute(query).fetchone()[0]
    pages_count = agents_count // 10

    if agents_count % 10 > 0:
        pages_count += 1

    return pages_count


def get_product_types() -> dict:
    query = select(ProductType.c.ID, ProductType.c.Title)
    types = engine.execute(query).fetchall()
    return types


def get_product_type_id_by_name(name):
    query = select(ProductType.c.ID).where(ProductType.c.Title == name)
    value = engine.execute(query).fetchone()
    return value


def save_file_in_folder(file: File, file_format: str) -> str:
    save_dir = directory+"\\data\\agents\\"
    now = datetime.datetime.now()
    dtm = now.strftime("%d-%B-%Y %H-%M-%S-%f")
    filename = f"{dtm}.{file_format}"
    db_path = f"/agents/{filename}"
    try:
        with open(os.path.join(save_dir, filename), 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except:
        return {
            "message": "There was an error uploading the file",
            "values":   {
                "curtime": now,
                "curdate": dtm,
                "filename": filename,
                "file_format":file_format,
            }
        }
    finally:
        file.file.close()
        return db_path

def get_file_from_db(file_path: str) -> File:
    file = File
    with open(directory+"/data"+file_path, encoding="utf-8", errors="ignore") as op_file:
        file = op_file.read()
    return file