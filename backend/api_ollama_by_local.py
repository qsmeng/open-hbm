import ollama
from ollama import Client

"""docs
https://github.com/ollama/ollama-python
https://github.com/ollama/ollama/blob/main/docs/openai.md
https://github.com/ollama/ollama/blob/main/docs/api.md
"""

model_name = "llama3.2:3b"
local_url = "http://localhost:11434"
# content_text = "this is a test"


def client(content_text):
    ollama.embed(model=model_name, input='The sky is blue because of rayleigh scattering')
    client = Client(host=local_url)
    response = client.chat(model=model_name, messages=[{'role': 'user', 'content': content_text}])
    print(response['message']['content'])
    return response['message']['content']