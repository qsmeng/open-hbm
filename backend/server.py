import logging
from fastapi import FastAPI
import uvicorn

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Half Black Money Server",
    version="1.0",
    description="A simple api server for Half Black Money game",
)

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
