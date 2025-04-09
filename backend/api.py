from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse, FileResponse
import os
import sys
import backend.login_or_register as login_or_register

# 添加项目根目录到 sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

router = APIRouter()

# ------------------------- 页面渲染相关路由 -------------------------
@router.get("/index")
async def index():
    """
    渲染首页页面。

    返回:
    - FileResponse: 返回index.html文件。
    """
    try:
        return FileResponse(os.path.join(project_root, "frontend/index.html"))
    except Exception as e:
        raise HTTPException(status_code=500, detail="出现错误，请稍后再试。")

@router.get("/index.html")
async def index_html():
    """
    重定向到首页。

    返回:
    - RedirectResponse: 重定向到/index路由。
    """
    return RedirectResponse(url="/index")

@router.get("/login")
async def login():
    """
    渲染登录页面。

    返回:
    - FileResponse: 返回login.html文件。
    """
    try:
        return FileResponse(os.path.join(project_root, "frontend/login.html"))
    except Exception as e:
        raise HTTPException(status_code=500, detail="无法加载登录页面，请稍后再试。")

@router.get("/login.html")
async def login_html():
    """
    重定向到登录页面。

    返回:
    - RedirectResponse: 重定向到/login路由。
    """
    return RedirectResponse(url="/login")

# ------------------------- 用户认证相关路由 -------------------------
@router.post("/login")
async def handle_login(request: Request):
    """
    处理用户登录请求。

    参数:
    - request: 包含登录数据的请求对象。

    返回:
    - dict: 包含登录结果和重定向URL的字典。
    """
    data = await request.json()
    response = await login_or_register.login(data)  # 确保传递 data 参数
    if "redirect_url" in response:
        return {"message": "登录成功", "redirect_url": response["redirect_url"]}
    return response

@router.post("/register")
async def handle_register(request: Request):
    """
    处理用户注册请求。

    参数:
    - request: 包含注册数据的请求对象。

    返回:
    - dict: 包含注册结果的字典。
    """
    data = await request.json()
    return await login_or_register.register(data)

@router.post("/forgot-password")
async def handle_forgot_password(request: Request):
    """
    处理忘记密码请求。

    参数:
    - request: 包含忘记密码数据的请求对象。

    返回:
    - dict: 包含忘记密码处理结果的字典。
    """
    data = await request.json()
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="邮箱地址不能为空")
    
    # 调用忘记密码逻辑
    result = await login_or_register.forgot_password(email)
    return result

# ------------------------- AI 服务相关逻辑 -------------------------
import backend.api_openai as api_openai
import backend.api_ollama_by_remoto as api_ollama_by_remoto
import backend.api_ollama_by_local as api_ollama_by_local

def client(api_type, content_text):
    """
    根据API类型调用相应的AI服务客户端。
    
    参数:
    - api_type: AI服务类型，可选值为 'openai', 'ollama_by_remoto', 'ollama_by_local'
    - content_text: 输入文本内容
    
    返回:
    - AI服务的响应结果，如果API类型无效则返回None
    """
    if api_type == 'openai':
        return api_openai.client(content_text)
    elif api_type == 'ollama_by_remoto':
        return api_ollama_by_remoto.client(content_text)
    elif api_type == 'ollama_by_local':
        return api_ollama_by_local.client(content_text)
    else:
        return None