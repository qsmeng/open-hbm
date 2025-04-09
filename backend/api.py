import backend.api_openai as api_openai
# import backend.api_ollama_by_openai as api_ollama_by_openai
import backend.api_ollama_by_remoto as api_ollama_by_remoto
import backend.api_ollama_by_local as api_ollama_by_local

def client(api_type,content_text):
    if api_type == 'openai':
        return api_openai.client(content_text)
    elif api_type == 'ollama_by_openai':
        return None
        # return api_ollama_by_openai.client(content_text)
    elif api_type == 'ollama_by_remoto':
        return api_ollama_by_remoto.client(content_text)
    elif api_type == 'ollama_by_local':
        return api_ollama_by_local.client(content_text)
    else:
        return None