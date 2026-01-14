from fastapi import APIRouter

from app.api.v1 import shell, supervisor, file

api_router = APIRouter()
api_router.include_router(shell.router, prefix="/shell", tags=["shell"])
api_router.include_router(supervisor.router, prefix="/supervisor", tags=["supervisor"])
api_router.include_router(file.router, prefix="/file", tags=["file"])
