from fastapi import APIRouter

from .api_base_agent import bm

debug_router = APIRouter()

@debug_router.get("/debug/getAgentTypeID/")
async def debug_agent_type_get_id(type: str = "ООО"):
    return bm.get_agent_type_id_by_name(type)

@debug_router.get("/debug/lastAgentID/")
async def debug_last_agent_id():
    return bm.get_last_agent_id()

@debug_router.get("/debug/getAgent/")
async def debug_get_agent(agent_id: int = 1):
    return bm.get_agent_by_id(agent_id)

@debug_router.get("/debug/agentSales/")
async def debug_agent_sales(agent_id: int = 1):
    return bm.get_sales_for_agent(agent_id)

@debug_router.get("/debug/getProductTypes/")
async def debug_product_types():
    return bm.get_product_types()

@debug_router.get("/debug/getProductTypeID/")
async def debug_product_type_get_id(type: str = "Спам"):
    return bm.get_product_type_id_by_name(type)