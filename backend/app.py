from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import sys

# 添加项目根目录到 sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

import backend.static as static

app = FastAPI(
    title="Half Black Money App",
    version="1.0",
    description="The main application for Half Black Money game",
)

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