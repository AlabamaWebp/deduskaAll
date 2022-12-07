from fastapi import HTTPException

import sqlalchemy as sa
from sqlalchemy import select, or_

from .base import Agent, AgentType, engine
from sqlalchemy import select


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


def get_type_by_name(type_name: str) -> int:
    query = select(AgentType.c.ID).where(AgentType.c.Title == type_name)
    value = engine.execute(query).fetchone()[0]
    if value == None:
        return HTTPException(
            detail="Invalid Value",
            headers={"Value error": "Name of type not in database"},
            status_code=400,
        )
    else:
        return value

def get_last_agent_id() -> int:
    query = select(sa.func.max(Agent.c.ID))
    value = engine.execute(query).fetchone()[0]
    if value == None:
        return 1
    return value


def get_pages_count(filters: dict) -> int:
    search_ = f"%{filters['search']}%"
    type_ = filters["ag_type"]
    
    query = select(sa.func.count(Agent.c.ID).label("Total")).where(
            or_(
                (Agent.c.Title.like(search_)), 
                (Agent.c.Phone.like(search_)),
                (Agent.c.Email.like(search_)),
            )
        )

    if type_ != 0:
        type_ = get_type_by_name(type_)
        query = query.where(Agent.c.AgentTypeID == type_)

    agents_count = engine.execute(query).fetchone()[0]
    pages_count = agents_count // 10

    if agents_count % 10 > 0:
        pages_count += 1

    return pages_count