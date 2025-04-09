from fastapi import APIRouter, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys

# 添加项目根目录到 sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

router = APIRouter()

# 挂载静态文件
router.mount("/static", StaticFiles(directory=os.path.join(project_root, "frontend")), name="static")

@router.get("/static/{filename:path}")
async def static_file(filename: str):
    """
    处理静态文件请求。

    参数:
    - filename: 请求的文件路径。

    返回:
    - FileResponse: 返回请求的静态文件。
    """
    frontend_path = os.path.join(project_root, "frontend", filename)
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    else:
            raise HTTPException(status_code=404, detail="File not found")
        



@router.get("/favicon.ico")
async def favicon():
    """
    处理网站图标请求。

    返回:
    - FileResponse: 返回网站图标文件。
    """
    favicon_path = os.path.join(project_root, "frontend/static/images/hbm.png")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    else:
        raise HTTPException(status_code=404, detail="Favicon not found")

