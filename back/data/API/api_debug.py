from fastapi import APIRouter, UploadFile, HTTPException, File

from .api_base_agent import bm
from ..settings import whitelist_image_formats

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

@debug_router.put("/debug/uploadFile/")
async def debug_upload_file(file: UploadFile = File(...)):
    file_format = file.filename.split(".")[-1]
    if file_format in whitelist_image_formats:
        return bm.save_file_in_folder(file, file_format)
    else:
        return HTTPException(
                status_code=400,
                detail="Invalid file format",
                headers={
                    "File error": f"Current file format({file_format}) not in whitelist"
                },
            )

@debug_router.get("/debug/getFile/")
async def debug_get_file(file_path = "/agents/agent_1.png"):
    return bm.get_file_from_db(file_path)