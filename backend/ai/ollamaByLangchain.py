def initialize_ollama_model(base_url: str, model_name: str) -> OllamaLLM:
    """
    初始化Ollama模型
    
    参数:
    - base_url: Ollama服务的基础URL
    - model_name: 要使用的模型名称
    
    返回:
    - OllamaLLM: 初始化后的模型实例
    """
    try:
        llm = OllamaLLM(
            base_url=base_url,
            model=model_name,
            temperature=0.7,
            top_p=0.9,
            timeout=DEFAULT_TIMEOUT
        )
        logger.info(f"成功初始化Ollama模型: {model_name}")
        return llm
    except Exception as e:
        logger.error(f"初始化Ollama模型失败: {e}")
        raise HTTPException(status_code=500, detail="模型初始化失败")

def create_tools() -> List[Tool]:
    """
    创建对话系统使用的工具集
    
    返回:
    - List[Tool]: 工具列表
    """
    tools = [
        Tool(
            name="search",
            func=lambda query: "搜索结果",  # TODO: 实现实际搜索功能
            description="用于搜索相关信息"
        ),
        Tool(
            name="calculator",
            func=lambda expr: str(eval(expr)),  # TODO: 实现更安全的计算
            description="用于执行数学计算"
        ),
        Tool(
            name="story_generator",
            func=lambda prompt: generate_story(prompt),
            description="用于生成故事内容"
        ),
        Tool(
            name="dialogue_manager",
            func=lambda message: manage_dialogue(message),
            description="用于管理对话流程"
        )
    ]
    return tools


def main():
    """
    主函数，启动AI对话服务
    """
    try:
        # 初始化模型
        llm = initialize_ollama_model(OLLAMA_BASE_URL, OLLAMA_MODEL_NAME)
        
        # 加载提示模板
        prompt = load_prompt_template()
        
        # 创建工具集
        tools = create_tools()
        
        # 创建对话agent
        agent = create_conversation_agent(llm, tools, prompt)
        
        # 启动FastAPI服务
        app = FastAPI()
        
        @app.post("/chat")
        async def chat_endpoint(request: Request):
            data = await request.json()
            user_input = data.get("message")
            if not user_input:
                raise HTTPException(status_code=400, detail="缺少消息内容")
            
            try:
                response = chat_with_agent(user_input, agent)
                return JSONResponse(content=response)
            except Exception as e:
                logger.error(f"对话处理失败: {e}")
                raise HTTPException(status_code=500, detail="对话处理失败")
        
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except Exception as e:
        logger.error(f"服务启动失败: {e}")
        raise


def test_chat_with_agent():
    """
    测试chat_with_agent函数
    """
    # 初始化模型
    llm = initialize_ollama_model(OLLAMA_BASE_URL, OLLAMA_MODEL_NAME)
    
    # 加载提示模板
    prompt = load_prompt_template()
    
    # 创建工具集
    tools = create_tools()
    
    # 创建对话agent
    agent = create_conversation_agent(llm, tools, prompt)
    
    # 测试对话
    test_message = "你好，你能帮我生成一个故事吗？"
    response = chat_with_agent(test_message, agent)
    
    assert isinstance(response, dict), "响应应为字典类型"
    assert "response" in response, "响应中应包含'response'字段"
    assert len(response["response"]) > 0, "响应内容不应为空"

def test_handle_generate_story():
    """
    测试handle_generate_story函数
    """
    theme = "冒险"
    characters = ["英雄", "恶龙"]
    
    response = handle_generate_story(theme, characters)
    
    assert isinstance(response, dict), "响应应为字典类型"
    assert "story" in response, "响应中应包含'story'字段"
    assert len(response["story"]) > 0, "故事内容不应为空"

def test_handle_manage_dialogue():
    """
    测试handle_manage_dialogue函数
    """
    message = "你好，你能帮我生成一个故事吗？"
    
    response = handle_manage_dialogue(message)
    
    assert isinstance(response, dict), "响应应为字典类型"
    assert "response" in response, "响应中应包含'response'字段"
    assert len(response["response"]) > 0, "响应内容不应为空"

if __name__ == "__main__":
    test_chat_with_agent()
    test_handle_generate_story()
    test_handle_manage_dialogue()
    print("所有测试通过！")
