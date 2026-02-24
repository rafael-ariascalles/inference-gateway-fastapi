from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from gateway.schema import InputRequest
from gateway.security import verify_token
from gateway.routes import app_router
import uuid
from gateway.config import get_settings


settings = get_settings()
ROOT_PATH = settings.root_path
API_TITLE = settings.api_title
REQUEST_ID_HEADER = settings.request_id_header

app = FastAPI(title=API_TITLE,root_path=ROOT_PATH)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    # HeaderDict is case-insensitive, so x-request-id / X-Request-Id both work
    request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4().hex)
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers[REQUEST_ID_HEADER] = request_id
    return response

app.include_router(app_router)

@app.get("/healthz", tags=["Checks"])
async def healthz():
    return {"status": "healthy"}

@app.get("/", tags=["Checks"])
async def ping():
    return {"status": "available"}
