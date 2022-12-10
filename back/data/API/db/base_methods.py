from fastapi import HTTPException

import sqlalchemy as sa
from sqlalchemy import select, or_
from sqlalchemy.engine import LegacyRow

from ..schemas.agent import AgentBase
from .base import Agent, AgentType,Product, ProductType, ProductSale, engine

def get_AgentBase_from_list(agent: list) -> AgentBase:
    if agent == None:
        return None
    return AgentBase(
            ag_id  = agent[0],
            ag_title = agent[1],
            ag_type = agent[2],
            ag_address = agent[3],
            ag_inn = agent[4],
            ag_kpp = agent[5],
            ag_director = agent[6],
            ag_phone = agent[7],
            ag_email = agent[8],
            ag_logo_path = agent[9],
            ag_priority = agent[10],
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
    query = select(Agent).where(Agent.c.ID == ag_id)
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