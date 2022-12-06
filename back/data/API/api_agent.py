import os

from fastapi import APIRouter, UploadFile, File

from .schemas.agent import AgentBase
from .schemas.agent import AgentFull

from .api_base import *


agent_router = APIRouter()



@agent_router.get("/agents/types/")
async def types_get():
    return get_agent_types()


@agent_router.get("/agents/{page}/")
async def agents_get(
        page: int = 1,
        type: str = "ООО",
        search: str = "%",
        order_by: int = 1,
        order: bool = True,
    ) -> list[AgentFull]:

    if page < 1:
        return HTTPException(
            status_code=400,
            detail="invalid page",
            headers={"page": "value must be positive"},
        )

    return base_agents_select(page, 
        {
            "search": search,
            "ag_type": type,
            "order": order,
            "order_by": order_by,
        }
    )


@agent_router.put("/agent/alter/one/")
async def agent_alter(ag_edited: AgentBase) -> int:
    return base_agent_update(ag_edited)

@agent_router.put("/agent/alter/multi/")
async def agent_alter_multi() -> int:
    return None

@agent_router.post("/agent/create/")
async def agent_create(agent: AgentBase) -> int:
    return base_agent_create(agent)

@agent_router.post("/agent/create/uploadfile/")
async def image_upload(agent_image: UploadFile(filename="agent_") = File(...)):
    if agent_image.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(400, detail="Invalid document type")
    return agent_image

@agent_router.delete("/agent/del/")
async def delete_agent(agent_id: int) -> bool:
    return None
