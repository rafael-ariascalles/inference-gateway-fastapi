from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from gateway.security import error_verify_token
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
    request_id = request.headers.get(REQUEST_ID_HEADER,str(uuid.uuid4().hex))
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers[REQUEST_ID_HEADER] = request_id
    return response

@app.get("/healthz", tags=["Checks"])
async def healthz():
    return {"status": "healthy"}

@app.get("/", tags=["Checks"])
async def ping():
    return {"status": "available"}



app.include_router(app_router,tags=["Chats"],dependencies=[Depends(error_verify_token)])



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"field": err["loc"][-1] if err["loc"] else "request", "message": err["msg"]}
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=400,
        content={"detail": {"errors": errors}},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("gateway.main:app", host="0.0.0.0", port=settings.port)