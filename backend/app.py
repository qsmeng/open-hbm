from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, FileResponse
import os
import sys

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

# 挂载api路由
app.include_router(api.router)

# 挂载静态文件路由
app.include_router(static.router)

@app.get("/")
async def root():
    """
    根路由，重定向到首页。

    返回:
    - RedirectResponse: 重定向到/index路由。
    """
    return RedirectResponse(url="/index")

@app.get("/get_character_templates")
async def get_character_templates():
    """
    获取角色模板（待实现）。

    返回:
    - dict: 角色模板数据（待实现）。
    """
    # 准备实现的逻辑
    pass

@app.get("/game")
async def game():
    """
    渲染游戏页面。

    返回:
    - FileResponse: 返回game.html文件。
    """
    try:
        return FileResponse(os.path.join(project_root, "frontend/game.html"))
    except Exception as e:
        raise HTTPException(status_code=500, detail="无法加载游戏页面，请稍后再试。")

@app.get("/get_story_templates")
async def get_story_templates():
    """
    获取故事模板（待实现）。

    返回:
    - dict: 故事模板数据（待实现）。
    """
    # 准备实现的逻辑
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)