from ollama import Client
from typing import Optional, List
from dotenv import load_dotenv
import os

"""docs ollama_by_local
https://github.com/ollama/ollama-python
https://github.com/ollama/ollama/blob/main/docs/openai.md
https://github.com/ollama/ollama/blob/main/docs/api.md
"""

# 加载环境变量
load_dotenv()

# 从配置文件 .env 获取 MODEL_NAME 和 LOCAL_OLLAMA_URL
LOCAL_OLLAMA_MODEL_NAME = os.getenv('LOCAL_OLLAMA_MODEL_NAME')
if not LOCAL_OLLAMA_MODEL_NAME:
    raise ValueError("环境变量 LOCAL_OLLAMA_MODEL_NAME 未设置")

LOCAL_OLLAMA_URL = os.getenv('LOCAL_OLLAMA_URL')
if not LOCAL_OLLAMA_URL:
    raise ValueError("环境变量 LOCAL_OLLAMA_URL 未设置")

# 单例客户端
_client = Client(host=LOCAL_OLLAMA_URL)

# 对话历史记录
conversation_history: List[dict] = []

def client(content_text: str) -> Optional[str]:
    """
    与本地Ollama服务进行交互的客户端函数。

    参数：
        content_text: 非空字符串，长度 <= 4096，表示用户输入的文本内容。
    返回：
        str: 模型响应内容，如果成功则返回生成的文本。
        None: 发生错误时返回None。
    """
    # 输入验证
    if not isinstance(content_text, str) or not content_text.strip():
        raise ValueError("content_text 必须是非空字符串")
    
    if len(content_text) > 4096:
        raise ValueError("输入长度超过 4096 字符限制")

    # 将用户消息添加到对话历史中
    conversation_history.append({'role': 'user', 'content': content_text})

    try:
        # 调用Ollama服务生成响应
        response = _client.chat(
            model=LOCAL_OLLAMA_MODEL_NAME,
            messages=conversation_history
        )
        result = response['message']['content']
        
        # 将助手消息添加到对话历史中
        conversation_history.append({'role': 'assistant', 'content': result})
        
        return result
    except Exception as e:
        print(f"API 调用失败: {str(e)}")
        return None

# test
# response = client('老狼老狼几点了')
# if response:
#     print(response)  # 或进行其他处理

# response = client('接下来会几点')
# if response:
#     print(response)  # 或进行其他处理
