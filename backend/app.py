import os
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# 将项目根目录添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.api import router as api_router

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载API路由
app.include_router(api_router, prefix="/api")

# 中间件：输出全部拦截到请求的请求url
@app.middleware("http")
async def log_request_url(request: Request, call_next):
    print(f"Request URL: {request.url}")
    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)