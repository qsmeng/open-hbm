from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os
import sys

class ContentSecurityPolicyMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        async def add_csp_headers(message):
            if message["type"] == "http.response.start":
                headers = message.get("headers", [])
                headers.append(
                    (b"Content-Security-Policy", (
                        b"default-src 'self'; "
                        b"script-src 'self' 'unsafe-inline' 'unsafe-eval' https://udify.app *.dify.dev *.dify.ai *.udify.app udify.app *.r2.cloudflarestorage.com *.sentry.io http://localhost:* http://127.0.0.1:* https://analytics.google.com googletagmanager.com *.googletagmanager.com https://www.google-analytics.com https://api.github.com 'nonce-NzE3Njg0M2EtZmYyNC00MDg3LTg4NDYtODI3MTA0OGYyZGJi'; "
                        b"style-src 'self' 'unsafe-inline'; "
                        b"img-src 'self' data: https://udify.app; "
                        b"connect-src 'self' https://udify.app; "
                        b"frame-src 'self' https://udify.app; "
                        b"font-src 'self'; "
                        b"object-src 'none'; "
                        b"base-uri 'self'; "
                        b"form-action 'self'; "
                        b"frame-ancestors 'self'; "
                        b"upgrade-insecure-requests;"
                    ))
                )
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, add_csp_headers)

# 添加项目根目录到 sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

import backend.api as api
import backend.static as static

app = FastAPI(
    title="Half Black Money App",
    version="1.0",
    description="The main application for Half Black Money game",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名访问
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)

# 添加CSP中间件
app.add_middleware(ContentSecurityPolicyMiddleware)

# 挂载api路由，并指定前缀为/api
app.include_router(api.router, prefix="/api")

# 挂载静态文件路由
app.include_router(static.router)

@app.get("/")
@app.get("/index")
async def root():
    """
    处理首页请求。

    返回:
    - FileResponse: 返回首页HTML文件。
    """
    try:
        frontend_index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "index", "index.html"))
        return FileResponse(frontend_index_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="首页文件未找到")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_character_templates")
async def get_character_templates():
    """
    获取角色模板。

    返回:
    - dict: 角色模板数据。
    """
    try:
        return await api.generate_template('character')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_story_templates")
async def get_story_templates():
    """
    获取故事模板。

    返回:
    - dict: 故事模板数据。
    """
    try:
        return await api.generate_template('story')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate_random_character")
async def generate_random_character():
    """
    生成随机角色。

    返回:
    - dict: 随机角色数据。
    """
    try:
        return await api.generate_random_character()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate_random_story")
async def generate_random_story():
    """
    生成随机故事。

    返回:
    - dict: 随机故事数据。
    """
    try:
        return await api.generate_random_story()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    健康检查端点。用于验证服务运行状况。
    
    返回:
    - dict: 服务健康状态。
    """
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)