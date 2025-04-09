import socket
import threading
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

def process_connection(client):
    """处理客户端连接"""
    try:
        # 接收客户端发来的数据
        data = b''
        while True:
            chunk = client.recv(1024)
            if not chunk:
                break
            data += chunk
            if len(chunk) < 1024:
                break

        logger.info(f'Received data from client: {data.decode("utf-8")}')

        # 给客户端发送响应数据
        response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hello World</h1>'
        client.sendall(response)
        logger.info('Response sent to client')

    except Exception as e:
        logger.error(f'Error processing connection: {str(e)}')
    finally:
        # 关闭客户端连接对象
        client.close()
        logger.info('Client connection closed')

def start_server():
    """启动服务器"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # 允许端口复用
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # 绑定 IP 和端口
            sock.bind(('127.0.0.1', 8000))
            # 开始监听
            sock.listen(5)
            logger.info('Server started and listening on port 8000')

            while True:
                # 等待客户端请求
                client, addr = sock.accept()
                logger.info(f'New connection from {addr}')

                # 创建新的线程来处理客户端连接
                t = threading.Thread(target=process_connection, args=(client,))
                t.start()

    except Exception as e:
        logger.error(f'Server error: {str(e)}')
    finally:
        logger.info('Server stopped')

def main():
    start_server()

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)