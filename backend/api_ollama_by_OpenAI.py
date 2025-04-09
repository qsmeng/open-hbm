from ollama import OpenAI 

def client(content_text):
    """
    通过OpenAI客户端与Ollama服务进行交互的客户端函数。

    参数：
        content_text: 用户输入的文本内容。
    返回：
        str: 模型响应内容，如果成功则返回生成的文本。
    """
    client = OpenAI(
        base_url='http://localhost:11434/v1/',
        api_key='ollama',  # 此处的api_key为必填项，但在ollama中会被忽略
    )
    chat_completion = client.chat.completions.create(
        messages=[{'role': 'user', 'content': content_text}],
        model='llama3.2:3b',
    ) 
    print(chat_completion.choices[0].text)
    return chat_completion.choices[0].text