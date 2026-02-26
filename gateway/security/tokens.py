from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging
from gateway.config import get_settings

settings = get_settings()
auth_scheme = HTTPBearer()
logger = logging.getLogger(__name__)
GATEWAY_API_KEY = settings.gateway_api_key

async def error_verify_token(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if token.credentials != GATEWAY_API_KEY:
        logger.error(f"Incorrect bearer token")
        raise HTTPException(
            status_code=401,
            detail={"errors": [{"message": "unauthorized"}]},
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True

async def verify_token(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if token.credentials != GATEWAY_API_KEY:
        return False
    return True
