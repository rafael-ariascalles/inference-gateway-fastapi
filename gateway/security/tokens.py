from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import status
import logging
import os

BACKEND_API_KEY = os.getenv("BACKEND_API_KEY", "NoKey")
auth_scheme = HTTPBearer()
logger = logging.getLogger(__name__)

async def error_verify_token(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if token.credentials != BACKEND_API_KEY:
        logger.error(f"Incorrect bearer token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect bearer token", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    return True

async def verify_token(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if token.credentials != BACKEND_API_KEY:
        return False
    return True