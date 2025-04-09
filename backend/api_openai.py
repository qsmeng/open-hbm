
# import get_remoto_api_url as api_url
import requests

# url = api_url.get_remoto_api_url("ollama")+'/v1/chat-messages'

local_url = 'http://localhost:11434/api/chat' 
url=local_url
api_key = '{api_key}'  # 替换为您的实际 API 密钥
ollama_api_key = 'ollama'  # 替换为您的实际 API 密钥

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

# content_text = 'Hello, how are you?'
model_name = 'llama3.2:3b'


def client(content_text):    
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