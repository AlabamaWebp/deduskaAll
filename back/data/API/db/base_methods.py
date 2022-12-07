from fastapi import HTTPException

import sqlalchemy as sa

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