# -*- coding: utf-8 -*-
"""
LangChain 对话 Agent 调用本地 Ollama 模型 (deepseek-r1:1.5b)
并使用记忆和rag等一系列工具构建一个完整的对话系统。
"""
import os
import re
from typing import List, Dict, Any
from langchain_ollama import OllamaLLM
from langchain.agents import create_react_agent, Tool, AgentExecutor
from langchain import hub
import logging
from typing import List, Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# 禁用默认追踪
os.environ["LANGCHAIN_HANDLER"] = ""

# 配置常量
OLLAMA_BASE_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL_NAME = os.getenv('OLLAMA_MODEL_NAME', 'deepseek-r1:1.5b')
DEFAULT_TIMEOUT = 30  # 默认超时时间(秒)
MAX_ITERATIONS = 5    # 最大迭代次数

def initialize_ollama_model(base_url: str, model_name: str) -> OllamaLLM:
    """
    初始化Ollama模型
    
    参数:
        base_url: Ollama服务地址
        model_name: 模型名称
        
    返回:
        OllamaLLM实例
        
    异常:
        ValueError: 当初始化失败时抛出
    """
    try:
        return OllamaLLM(
            base_url=base_url,
            model=model_name,
            timeout=DEFAULT_TIMEOUT,
            temperature=0.1  # 降低温度，使输出更确定
        )
    except Exception as e:
        logger.error(f"初始化Ollama模型失败: {e}")
        raise ValueError(f"无法初始化Ollama模型: {e}")

def load_prompt_template():
    """加载提示模板"""
    try:
        return hub.pull("hwchase17/react")
    except Exception as e:
        logger.error(f"加载提示模板失败: {e}")
        raise

def sanitize_input(input_str: str) -> str:
    """
    清理输入文本，防止潜在的安全问题
    
    参数:
        input_str: 待清理的文本
        
    返回:
        清理后的安全文本
    """
    return re.sub(r"[;'\"\\]", "", input_str.strip())

def create_tools() -> List[Tool]:
    """创建工具列表"""
    return [
        Tool(
            name="ExampleTool",
            func=lambda x: f"Echo: {sanitize_input(x)}",
            description="一个简单的工具，回显输入内容"
        )
    ]

def create_conversation_agent(llm: OllamaLLM, tools: List[Tool], prompt) -> AgentExecutor:
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    
    def handle_error(error: Exception, input: str) -> str:
        """自定义解析错误处理函数"""
        logger.warning(f"代理解析错误: {error}\n输入内容: {input}")
        return "我无法理解当前步骤，请重新描述您的需求。"
    
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        llm=llm,
        verbose=True,
        handle_parsing_errors=handle_error,
        max_iterations=5  # 添加最大迭代次数限制
    )

def chat_with_agent(user_prompt: str, agent: AgentExecutor) -> Dict[str, Any]:
    """
    与代理进行对话
    
    参数:
        user_prompt: 用户输入
        agent: 代理实例
        
    返回:
        包含状态和响应的字典:
        {
            "status": "success"|"error",
            "response": str,  # 成功时
            "message": str    # 错误时
        }
    """
    try:
        logger.info(f"处理用户输入: {user_prompt}")
        response = agent.invoke(
            {"input": user_prompt},
            config={"timeout": DEFAULT_TIMEOUT}
        )
        return {"status": "success", "response": response}
    except Exception as e:
        logger.error(f"对话处理失败: {e}")
        return {"status": "error", "message": str(e)}

def main():
    """主程序入口"""
    try:
        logger.info("初始化对话系统...")
        
        # 初始化组件
        ollama_model = initialize_ollama_model(OLLAMA_BASE_URL, OLLAMA_MODEL_NAME)
        prompt = load_prompt_template()
        tools = create_tools()
        agent = create_conversation_agent(ollama_model, tools, prompt)
        
        logger.info("对话系统初始化完成，准备接收输入")
        
        # 示例对话
        test_inputs = [
            "你好，对话代理！",
            "你能做什么？",
            "请介绍一下你自己"
        ]
        
        for user_input in test_inputs:
            response = chat_with_agent(user_input, agent)
            if response["status"] == "success":
                print(f"\n用户: {user_input}")
                print(f"代理: {response['response']}")
            else:
                print(f"对话出错: {response['message']}")
                
    except Exception as e:
        logger.critical(f"系统初始化失败: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
