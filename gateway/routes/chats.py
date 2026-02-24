from fastapi import APIRouter
from gateway.schema import InputRequest

router = APIRouter()

@router.post("/v1/chat/completions")
async def chat_completions(inputs: InputRequest):
    if inputs.stream:
        return await streaming(inputs)
    else:
        return await generate(inputs)

async def streaming(inputs: InputRequest):
    return {"status": "available"}

async def generate(inputs: InputRequest):
    return {"status": "available"}