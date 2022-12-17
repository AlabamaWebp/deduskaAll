from fastapi import HTTPException, APIRouter, UploadFile, File

from .schemas.agent import AgentMain, AgentGet, AgentPostDB

from .api_base_agent import bm, base_agents_select, base_agent_create, base_agent_update, base_agent_delete, base_agent_priority_update


agent_router = APIRouter()



@agent_router.get("/agent/types/")
async def types_get():
    return bm.get_agent_types()

@agent_router.get("/agent/pages/")
async def get_total_pages(
        type_: str = "0",
        search: str = "%",
    ) -> int:

    return bm.get_pages_count({
        "search": search,
        "ag_type": type_
    })

@agent_router.get("/agent/{page}/")
async def agents_get(
        page: int = 1,
        type_: str = "0",
        search: str = "%",
        order_by: int = 1,
        order: bool = True,
    ) -> list[AgentGet]:

    if page < 1:
        return HTTPException(
            status_code=400,
            detail="invalid page",
            headers={"page": "value must be positive"},
        )

    return base_agents_select(page, 
        {
            "search": search,
            "ag_type": type_,
            "order": order,
            "order_by": order_by,
        }
    )

@agent_router.put("/agent/edit/one/")
async def agent_alter(
        agent: AgentMain,
        # file: UploadFile = File(...),
    ) -> int:
    agent = AgentPostDB(agent)
    # agent.ag_logo_path = bm.save_file_in_folder(file)
    return base_agent_update(agent)

@agent_router.put("/agent/edit/multi/")
async def agent_alter_multi(ag_id: list[int], priority: int) -> int:
    return base_agent_priority_update(ag_id, priority)

@agent_router.post("/agent/create/")
async def agent_create(
        agent: AgentPostDB,
        # file: UploadFile = File(...),
    ) -> int:
    # agent.ag_logo_path = bm.save_file_in_folder(file)
    return base_agent_create(agent)

# @agent_router.post("/agent/create/uploadfile/")
# async def image_upload(agent_image: UploadFile(filename="agent_") = File(...)):
#     pass
#     # if agent_image.content_type not in ["image/png", "image/jpeg"]:
#     #     raise HTTPException(400, detail="Invalid document type")
#     # return agent_image

@agent_router.delete("/agent/del/")
async def delete_agent(agent_id: int) -> bool:
    return base_agent_delete(agent_id)