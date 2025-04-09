from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys

# 添加项目根目录到 sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

router = FastAPI()

# 挂载静态文件
router.mount("/static", StaticFiles(directory=os.path.join(project_root, "frontend/static")), name="static")

@router.get("/static/{filename:path}")
async def static_file(filename: str):
    """
    处理静态文件请求。

    参数:
    - filename: 请求的文件路径。

    返回:
    - FileResponse: 返回请求的静态文件。
    """
    return FileResponse(os.path.join(project_root, "frontend/static", filename))

@router.get("/favicon.ico")
async def favicon():
    """
    处理网站图标请求。

    返回:
    - FileResponse: 返回网站图标文件。
    """
    try:
        return FileResponse(os.path.join(project_root, "frontend/static/images/hbm.png"))
    except Exception as e:
        raise HTTPException(status_code=500, detail="无法加载图标，请稍后再试。")
