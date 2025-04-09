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

async def ollama_client(content_text: str, context: Optional[dict] = None) -> Optional[str]:
    """
    与Ollama服务交互以生成AI响应。

    描述：
        此方法通过调用Ollama服务的聊天接口，生成用户文本输入的响应文本。

    参数：
        content_text (str): 用户输入文本，必须为非空字符串且长度不超过4096字符。
        context (Optional[dict], 可选): 附加上下文信息字典，如角色信息或故事背景。

    返回：
        Optional[str]: 若调用成功，返回Ollama生成的文本。若失败，则返回None。

    异常：
        ValueError: 若输入文本为空或超出长度限制时，抛出此异常。
        Exception: 任何调用Ollama服务失败时触发，并记录错误信息。
    """
    # 输入验证
    if not isinstance(content_text, str) or not content_text.strip():
        raise ValueError("content_text 必须是非空字符串")
    
    if len(content_text) > 4096:
        raise ValueError("输入长度超过 4096 字符限制")

    # 初始化对话历史
    messages = [{'role': 'user', 'content': content_text}]

    # 如果有上下文信息，将其添加到对话历史中
    if context:
        messages.append({'role': 'system', 'content': f"上下文信息: {str(context)}"})

    try:
        # 调用Ollama服务生成响应
        client = Client(host=OLLAMA_URL)
        response = client.chat(
            model=OLLAMA_MODEL_NAME,
            messages=messages
        )
        result = response['message']['content']
        # 如果 result 是字典对象，则将其转换为字符串
        if isinstance(result, dict):
            result = str(result)
        
        return result
    except Exception as e:
        print(f"API 调用失败: {str(e)}")
        # 添加详细错误日志
        print(f"请检查以下配置：")
        print(f"OLLAMA_URL: {OLLAMA_URL}")
        print(f"OLLAMA_MODEL_NAME: {OLLAMA_MODEL_NAME}")
        print(f"确保服务正在运行并监听端口 {OLLAMA_URL.split(':')[-1]}")
        return None
# 注释掉测试代码
# content_text = "this is a test"
# re=ollama_client(content_text)
# print("Ollama_client:"+re)

# 注释掉硬编码的环境变量，使用.env文件中的配置
# OLLAMA_MODEL_NAME = "deepseek-r1:1.5b"
# OLLAMA_URL = "127.0.0.1:11434"

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