# uvicorn --reload main:app --host 26.246.185.101 --port 8000

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from fastapi.middleware.cors import CORSMiddleware

from data.API.api_agent import agent_router
from data.API.api_debug import debug_router

from data.API.db.base import create_tables_if_not_exists as CTINE


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def create_tables():
    CTINE()

@app.get("/")
async def main_page():
    return RedirectResponse(url="/docs/", status_code=307)

app.include_router(agent_router)

app.include_router(debug_router)