import sqlalchemy as sa

from fastapi import HTTPException

from sqlalchemy import select, delete, update, insert
from sqlalchemy import or_, and_
from sqlalchemy.sql import func
from .db.base import Agent, AgentType, Product, ProductType, ProductSale, engine

from .schemas.agent import AgentBase
from .schemas.agent import AgentFull
from .db.base_methods import *

time_offset = 10

def base_agents_select(page: int, filters: dict) -> list[AgentFull]:

    search_ = f"%{filters['search']}%"
    type_ = filters["ag_type"]
    order_ = filters["order"]
    order_by_ = filters["order_by"]

    query = select(
            Agent.c.ID,
            Agent.c.Title,
            Agent.c.DirectorName,
            Agent.c.Address,
            Agent.c.Phone,
            Agent.c.INN,
            Agent.c.KPP,
            Agent.c.Email,
            Agent.c.Logo,
            Agent.c.Priority,
            select(AgentType.c.Title).where(
                    Agent.c.AgentTypeID == AgentType.c.ID
                ).label("AgentType"),
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
        ).where(
            or_(
                (Agent.c.Title.like(search_)), 
                (Agent.c.Phone.like(search_)),
                (Agent.c.Email.like(search_)),
            )
        )

    if type_ != 0:
        type_ = get_type_by_name(type_)
        query = query.where(Agent.c.AgentTypeID == type_)

    order = Agent.c.Title
    match order_by_:
            case 1:
                order = Agent.c.Title
            case 2:
                order = Agent.c.Priority
            case 3:
                order = sa.Column("AnnualSalesBy")
                
    if order_:
        query = query.order_by(order)
    else:
        query = query.order_by(order.desc())

    query = query.offset(page*10-10).limit(10)
    values = engine.execute(query).fetchall()

    out_values = []

    for ag in values:
        
        with open("data\\" + ag[8], "rb") as img_byte:
                image_b = img_byte.read()
                image_b = f"{image_b}"

        return_values = AgentFull(
            ag_id  = ag[0],
            ag_title = ag[1],
            ag_director = ag[2],
            ag_address = ag[3],
            ag_phone = ag[4],
            ag_inn = ag[5],
            ag_kpp = ag[6],
            ag_email = ag[7],
            ag_logo_path = ag[8],
            ag_priority = ag[9],
            ag_type = ag[10],
            ag_sales = ag[11],
            ag_disc = ag[12],
            ag_logo_bytes = image_b,
        )
        out_values.append(return_values)
    return out_values

def base_agent_update(agent: AgentBase):
    type_id = get_type_by_name(agent.ag_type)

    try:
        if type_id.status_code:
            return type_id
    except:
        pass

    query = update(Agent).values(
        Title = agent.ag_title,
        AgentTypeID = type_id,
        Address = agent.ag_address,
        INN = agent.ag_inn,
        KPP = agent.ag_kpp,
        DirectorName = agent.ag_director,
        Phone = agent.ag_phone,
        Email = agent.ag_email,
        Logo = agent.ag_logo_path,
        Priority = agent.ag_priority,
    ).where(Agent.c.ID == agent.ag_id)
    value = engine.execute(query)
    return value


def base_agent_create(agent: AgentBase):
    type_id = get_type_by_name(agent.ag_type)

    query = insert(Agent).values(
        ID = str(get_last_agent_id() + 1),
        Title = agent.ag_title,
        AgentTypeID = type_id,
        Address = agent.ag_address,
        INN = agent.ag_inn,
        KPP = agent.ag_kpp,
        DirectorName = agent.ag_director,
        Phone = agent.ag_phone,
        Email = agent.ag_email,
        Logo = agent.ag_logo_path,
        Priority = agent.ag_priority,
    )
    value = engine.execute(query)
    return value