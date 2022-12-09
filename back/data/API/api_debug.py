from fastapi import APIRouter

from .api_base import bm

debug_router = APIRouter()

@debug_router.get("/debug/agentType/{type}/")
async def debug_agent_type_get_id(type: str):
    return bm.get_type_by_name(type)

@debug_router.get("/debug/lastAgentID/")
async def debug_last_agent_id():
    return bm.get_last_agent_id()

@debug_router.get("/debug/getAgent/")
async def debug_get_agent(agent_id: int):
    return bm.get_agent_by_id(agent_id)

@debug_router.get("/debug/agentSales/")
async def debug_agent_sales(agent_id: int):
    return bm.get_sales_for_agent(agent_id)