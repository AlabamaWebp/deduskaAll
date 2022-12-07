from fastapi import APIRouter

from .api_base import *

debug_router = APIRouter()

@debug_router.get("/debug/agentType/{type}/")
async def debug_agent_type_get_id(type: str):
    return get_type_by_name(type)

@debug_router.get("/debug/lastAgentID/")
async def debug_last_agent_id():
    return get_last_agent_id()