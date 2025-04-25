from fastapi import APIRouter
from .modules.auth import router as auth_router

router = APIRouter()

# 注册认证路由 拦截 api/auth 请求
router.include_router(auth_router, prefix="/auth", tags=["auth"])