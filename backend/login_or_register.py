from db.hbm_db import get_db_connection
import logging
import re
from fastapi import HTTPException
import bcrypt

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 正则表达式模式
USERNAME_PATTERN = r'^[a-zA-Z0-9_]{4,20}$'
PASSWORD_PATTERN = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
EMAIL_PATTERN = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def validate_input(username, password, email):
    """
    验证输入数据的有效性。

    参数:
    - username: 用户名，4-20位字母、数字或下划线组合。
    - password: 密码，至少8位，包含字母和数字。
    - email: 邮箱地址，需符合标准格式。

    返回:
    - (bool, str): 验证结果和错误消息。
    """
    if not re.match(USERNAME_PATTERN, username):
        return False, "用户名必须为4-20位的字母、数字或下划线组合"
    
    if not re.match(PASSWORD_PATTERN, password):
        return False, "密码必须至少8位，且包含字母和数字"
    
    if not re.match(EMAIL_PATTERN, email):
        return False, "邮箱格式不正确"
    
    return True, None

async def register(data: dict):
    """
    注册新用户。

    参数:
    - data: 包含用户信息的字典，包括用户名、密码和邮箱。

    返回:
    - dict: 表示注册结果的字典。

    抛出:
    - HTTPException: 如果输入无效或注册过程失败。
    """
    try:
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        # 输入验证
        is_valid, error_message = validate_input(username, password, email)
        if not is_valid:
            logger.warning(f"Invalid input: {error_message}")
            raise HTTPException(status_code=400, detail=error_message)

        # 检查用户名是否已存在
        with get_db_connection() as conn, conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM user_base_info WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                logger.warning(f"Username already exists: {username}")
                raise HTTPException(status_code=400, detail="用户名已存在")

            # 对密码进行哈希处理
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # 插入新用户
            cursor.execute(
                "INSERT INTO user_base_info (username, password_hash, email) VALUES (%s, %s, %s)",
                (username, password_hash, email)
            )
            conn.commit()
            logger.info(f"User {username} registered successfully")
            return {"message": "注册成功"}
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail="注册失败，请稍后再试")

async def login(data: dict):
    """
    用户登录验证。

    参数:
    - data: 包含登录信息的字典，包括用户名和密码。

    返回:
    - dict: 登录成功时返回包含消息和重定向URL的字典。

    抛出:
    - HTTPException: 如果用户名不存在或密码错误。
    """
    username = data.get('username')
    password = data.get('password')

    # 验证用户名和密码
    with get_db_connection() as conn, conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM user_base_info WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            logger.info(f"User {username} logged in successfully")
            return {"message": "登录成功", "redirect_url": "/index"}  # 添加重定向URL
        else:
            logger.warning(f"Login failed for user: {username}")
            raise HTTPException(status_code=401, detail="用户名或密码错误")

async def forgot_password(email: str):
    """
    处理忘记密码请求。

    参数:
    - email: 用户的邮箱地址。

    返回:
    - dict: 包含重置密码链接的消息。

    抛出:
    - HTTPException: 如果邮箱格式无效、邮箱未注册或处理过程失败。
    """
    try:
        # 验证邮箱格式
        if not re.match(EMAIL_PATTERN, email):
            raise HTTPException(status_code=400, detail="邮箱格式不正确")

        # 检查邮箱是否存在
        with get_db_connection() as conn, conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM user_base_info WHERE email = %s", (email,))
            user = cursor.fetchone()

            if not user:
                raise HTTPException(status_code=404, detail="邮箱未注册")

            # 生成重置密码链接（示例，实际应用中应生成唯一令牌）
            reset_link = f"https://example.com/reset-password?email={email}"
            logger.info(f"Reset password link generated for {email}: {reset_link}")

            # 发送重置密码链接（示例，实际应用中应通过SMTP发送邮件）
            logger.info(f"Reset password link sent to {email}")

            return {"message": "重置密码链接已发送到您的邮箱"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error during forgot password process: {str(e)}")
        raise HTTPException(status_code=500, detail="处理忘记密码请求时出错，请稍后再试")