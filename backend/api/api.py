from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List
from db.hbm_db import get_db_connection

router = APIRouter()

class Card(BaseModel):
    id: str
    name: str
    description: str
    image_url: str

@router.get("/cards", response_model=List[Card])
async def get_cards():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT card_uuid, card_name, card_details, card_image_url FROM card_info")
    cards = cursor.fetchall()
    conn.close()
    return [{"id": card[0], "name": card[1], "description": card[2], "image_url": card[3]} for card in cards]

@router.post("/cards")
async def create_card(card: Card):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO card_info (card_uuid, card_name, card_details, card_image_url) VALUES (%s, %s, %s, %s)",
        (card.id, card.name, card.description, card.image_url)
    )
    conn.commit()
    conn.close()
    return {"message": "Card created successfully"}

@router.delete("/cards/{card_id}")
async def delete_card(card_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM card_info WHERE card_uuid = %s", (card_id,))
    conn.commit()
    conn.close()
    return {"message": "Card deleted successfully"}

# 导入 login_or_register 模块
from backend.auth import login_or_register

# ------------------------- 用户认证相关路由 -------------------------
@router.post("/login")
async def handle_login(request: Request):
    """
    处理用户登录请求。

    参数:
    - request: 包含登录数据的请求对象。

    返回:
    - dict: 包含登录结果和重定向URL的字典。
    """
    data = await request.json()
    response = await login_or_register.login(data)  # 确保传递 data 参数
    if "redirect_url" in response:
        return {"message": "登录成功", "redirect_url": response["redirect_url"]}
    return response

@router.post("/register")
async def handle_register(request: Request):
    """
    处理用户注册请求。

    参数:
    - request: 包含注册数据的请求对象。

    返回:
    - dict: 包含注册结果的字典。
    """
    data = await request.json()
    return await login_or_register.register(data)

@router.post("/forgot-password")
async def handle_forgot_password(request: Request):
    """
    处理忘记密码请求。

    参数:
    - request: 包含忘记密码数据的请求对象。

    返回:
    - dict: 包含忘记密码处理结果的字典。
    """
    data = await request.json()
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="邮箱地址不能为空")

    # 调用忘记密码逻辑
    try:
        result = await login_or_register.forgot_password(email)
        return result
    except Exception as e:
        print(f"处理忘记密码请求时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail="处理忘记密码请求时发生内部错误")

@router.post("/logout")
async def handle_logout(request: Request):
    """
    处理用户登出请求。

    参数:
    - request: 包含登出数据的请求对象。

    返回:
    - dict: 包含登出结果的字典。
    """
    # 调用登出逻辑
    result = await login_or_register.logout(request)
    return result

@router.post("/update-profile")
async def handle_update_profile(request: Request):
    """
    处理用户更新个人资料请求。

    参数:
    - request: 包含更新个人资料数据的请求对象。

    返回:
    - dict: 包含更新结果的字典。
    """
    data = await request.json()
    result = await login_or_register.update_profile(data)
    return result

@router.post("/update-preferences")
async def handle_update_preferences(request: Request):
    """
    处理用户更新偏好设置请求。

    参数:
    - request: 包含更新偏好设置数据的请求对象。

    返回:
    - dict: 包含更新结果的字典。
    """
    data = await request.json()
    result = await login_or_register.update_preferences(data)
    return result

@router.post("/submit-feedback")
async def handle_submit_feedback(request: Request):
    """
    处理用户提交反馈请求。

    参数:
    - request: 包含反馈数据的请求对象。

    返回:
    - dict: 包含反馈提交结果的字典。
    """
    data = await request.json()
    result = await login_or_register.submit_feedback(data)
    return result

@router.get("/notifications")
async def handle_get_notifications(request: Request):
    """
    处理用户获取通知请求。

    参数:
    - request: 包含获取通知数据的请求对象。

    返回:
    - dict: 包含通知列表的字典。
    """
    result = await login_or_register.get_notifications(request)
    return result

# ------------------------- AI 服务相关逻辑 -------------------------
import backend.api.api_ollama as api_ollama

@router.post("/chat")
async def handle_chat(request: Request):
    """
    处理用户聊天消息。

    参数:
    - request: 包含聊天数据的请求对象。

    返回:
    - dict: 包含AI生成响应的字典。
    """
    data = await request.json()
    message = data.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="消息不能为空")

    print(f"处理聊天请求，用户消息: {message}")
    try:
        response = await api_ollama.ollama_client(message)
        if response is None:
            raise HTTPException(status_code=500, detail="AI服务生成响应失败")
        print(f"AI响应: {response}")
        return {"message": response}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"处理聊天请求时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail="处理聊天请求时发生内部错误")

@router.get("/generate_story_background")
async def handle_generate_story_background(role: str, game_progress: str):
    """
    生成故事背景。

    参数:
    - role: 当前角色身份。
    - game_progress: 当前游戏进程。

    返回:
    - dict: 包含生成的故事背景文本的字典。
    """
    if not role or not game_progress:
        raise HTTPException(status_code=400, detail="角色和游戏进程不能为空")

    # 调用生成故事背景函数，并添加日志
    print(f"生成故事背景，角色: {role}, 游戏进程: {game_progress}")
    story_background = api_ollama.generate_story_background(role, game_progress)
    if not story_background:
        raise HTTPException(status_code=500, detail="生成故事背景失败")
    print(f"生成的故事背景: {story_background}")
    return {"story_background": story_background}