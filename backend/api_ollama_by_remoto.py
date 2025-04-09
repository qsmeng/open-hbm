# import get_remoto_api_url
import ollama
from ollama import Client

"""docs
https://github.com/ollama/ollama-python
https://github.com/ollama/ollama/blob/main/docs/openai.md
https://github.com/ollama/ollama/blob/main/docs/api.md
"""

model_name = "llama3.2:3b"
# ollama_api_url = api_url.get_remoto_api_url("ollama")
ollama_api_url = "https://501c3722.r12.vip.cpolar.cn"
# content_text = "this is a test"

def client(content_text):
    ollama.embed(model=model_name, input='The sky is blue because of rayleigh scattering')
    client = Client(host=ollama_api_url)
    response = client.chat(model=model_name, messages=[{'role': 'user', 'content': content_text}])
    print(response['message']['content'])
    return response['message']['content']

# async_chat
# async def client():
#   message = {'role': 'user', 'content': 'Why is the sky blue?'}
#   try:
#     asyncClient = ollama.AsyncClient(host=local_url)
#     async for part in await asyncClient.chat(model=model_name, messages=[message], stream=True):
#       print(part['message']['content'], end='', flush=True)
#   except ollama.ResponseError as e:
#     print('Error:', e.error)

# asyncio.run(async_chat())