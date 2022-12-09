from fastapi import HTTPException, APIRouter, UploadFile, File

from .schemas.agent import AgentBase
from .schemas.agent import AgentFull

from .api_base import bm


product_router = APIRouter()

# @product_router.get("/products/get/")