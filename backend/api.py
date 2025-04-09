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

# 从配置文件 .env 获取 MODEL_NAME 和 OLLAMA_URL
OLLAMA_MODEL_NAME = os.getenv('OLLAMA_MODEL_NAME')
if not OLLAMA_MODEL_NAME:
    raise ValueError("环境变量 OLLAMA_MODEL_NAME 未设置")

# OLLAMA_URL = api_url.get_remoto_api_url("ollama")
# OLLAMA_URL = "https://501c3722.r12.vip.cpolar.cn"
OLLAMA_URL = os.getenv('OLLAMA_URL')
if not OLLAMA_URL:
    raise ValueError("环境变量 OLLAMA_URL 未设置")

# 对话历史记录
conversation_history: List[dict] = []

from openai import OpenAI  # 新增导入
async def OpenAIAPI_Ollama_client(content_text: str) -> Optional[str]:
    """
    使用OpenAIAPI与Ollama服务交互以生成AI响应。

    描述：
        此方法通过OpenAIAPI的接口与Ollama服务交互，发送用户的文本输入并获取生成的响应。

    参数：
        content_text (str): 待处理的用户输入文本，必须为非空字符串且长度不超过4096字符。

    返回：
        Optional[str]: 成功时返回响应文本内容，失败时返回None。

    异常：
        ValueError: 当输入文本无效（为空或超长度限制）时抛出。
        Exception: 当服务调用失败或返回错误时抛出，并提供详细的错误日志。
    """
    # 输入验证
    if not isinstance(content_text, str) or not content_text.strip():
        raise ValueError("content_text 必须是非空字符串")
    
    if len(content_text) > 4096:
        raise ValueError("输入长度超过 4096 字符限制")

    try:
        # 打印调试信息
        print(f"尝试连接到Ollama服务，base_url: http://{OLLAMA_URL}/v1/")
        client = OpenAI(
            base_url=f'http://{OLLAMA_URL}/v1/',  # 确保使用完整的URL
            api_key='ollama',
        )
        chat_completion = await client.chat.completions.create(
            messages=[{'role': 'user', 'content': content_text}],
            model=OLLAMA_MODEL_NAME  # 使用环境变量
        )
        # 清理模型响应内容，移除多余的空行和无关信息
        response_content = chat_completion.choices[0].message.content
        cleaned_response = "\n".join(line.strip() for line in response_content.splitlines() if line.strip())
        print(f"成功获取模型响应: {cleaned_response}")
        return cleaned_response
    except Exception as e:
        print(f"API 调用失败: {str(e)}")
        # 添加详细错误日志
        print(f"请检查本地Ollama服务是否已启动，并确认以下配置：")
        print(f"base_url: http://{OLLAMA_URL}/v1/")
        print(f"model: {OLLAMA_MODEL_NAME}")
        print(f"确保服务正在运行并监听端口 {OLLAMA_URL.split(':')[-1]}")
        return None

# 注释掉测试代码
# content_text = "this is a test"
# re=OpenAIAPI_Ollama_client(content_text)
# print("OpenAIAPI_Ollama_client:"+re)