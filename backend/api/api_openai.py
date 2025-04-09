
import requests
import os

# Use environment variable for API key
api_key = os.getenv('OPENAI_API_KEY', 'your_default_api_key_here')

# URL for the API endpoint
url = 'http://localhost:11434/api/chat'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

# content_text = 'Hello, how are you?'
model_name = 'llama3.2:3b'


def client(content_text):    
    """
    通过OpenAI API与Ollama服务进行交互的客户端函数。

    参数：
        content_text: 用户输入的文本内容。
    返回：
        dict: 模型响应内容，如果成功则返回生成的JSON数据。
    """
    # 要发送的数据
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": content_text
            }
        ],
        "stream": False
    } 
    # 发送 POST 请求
    response = requests.post(url, json=data) 
    # 打印响应内容
    print(response.text)
    return response.json()

# TODO: 实现卡牌管理功能，允许玩家存储和管理卡牌信息