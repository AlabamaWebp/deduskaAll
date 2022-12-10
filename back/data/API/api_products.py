from fastapi import HTTPException, APIRouter, UploadFile, File

from .schemas.agent import AgentBase
from .schemas.agent import AgentFull

from .api_base_agent import bm
from .api_base_product import get_product_sales_for_agent


product_router = APIRouter()

@product_router.get("/products/get/")
async def get_sales_for_agent(ag_id: int = 1):
    return get_product_sales_for_agent(ag_id)