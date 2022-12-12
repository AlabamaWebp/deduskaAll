import io
from PIL import Image as pimg

import sqlalchemy as sa

from fastapi import HTTPException

from sqlalchemy import select, delete, update, insert
from sqlalchemy import or_, and_
from sqlalchemy.sql import func
from .db.base import Agent, AgentType, Product, ProductSale, engine

from .schemas.agent import AgentBase
from .schemas.agent import AgentFull
from .db import base_methods as bm

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

    if type_ != "0":
        type_ = bm.get_agent_type_id_by_name(type_)
        if type_ == None:
            return HTTPException(
                status_code=400,
                detail="Invalid Value",
                headers={"Invalid value": "Name of type is not in database"},
            )
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
        
        image_b = ""
        # with pimg.open("data\\" + ag[8]) as img:
        #         image_b = f"{img.tobytes()}"

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
            ag_disc = bm.recount_discount(ag[12]),
            ag_logo_bytes = image_b,
        )
        out_values.append(return_values)

    return out_values

def base_agent_update(agent: AgentBase):
    type_id = bm.get_agent_type_id_by_name(agent.ag_type)

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

def base_agent_priority_update(ag_id: list[int], tgt_priority: int):
    for id in ag_id:
        if id <= 0:
            return HTTPException(400, 
                detail="No agents with negative or 0 ids",
                headers={"Value error": "No agents with negative or 0 ids"}
            )

    if not len(ag_id):
        return HTTPException(400,
            detail="No agents in list",
            headers={"Value error": "No selected agents"}
        )

    if not int(tgt_priority):
        return HTTPException(400,
            detail="Target priority is not a value",
            headers={"Value error": "Priority is not integer"}
        )
    
    if tgt_priority <= 0:
        return HTTPException(400,
            detail="Target priority is negative",
            headers={"Value error": "Priority is negative"}
        )

    query = update(Agent).values(Priority = tgt_priority).where(Agent.c.ID.in_(ag_id))
    edited = engine.execute(query).fetchall()
    return edited

def base_agent_create(agent: AgentBase):
    type_id = bm.get_agent_type_id_by_name(agent.ag_type)

    query = insert(Agent).values(
        ID = str(bm.get_last_agent_id() + 1),
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

def base_agent_delete(agent_id: int):
    if len(bm.get_sales_for_agent(agent_id)) == 0:
        if bm.get_agent_by_id(agent_id) != None:
            query = delete(Agent).where(Agent.c.ID == agent_id)
            engine.execute(query)
            return True
        else:
            return HTTPException(
                status_code=400,
                detail="No agent with this ID",
                headers={
                    "Value error": "No agent with this ID"
                },
            )
    else:
        return HTTPException(
            status_code=202,
            detail="This agent has sales",
            headers={
                "Deletion denied": "Agent has sales"
            },
        )
    