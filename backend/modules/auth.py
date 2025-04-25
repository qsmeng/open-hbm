from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
import mysql.connector
from backend.database.hbm_mysql import get_db_connection

router = APIRouter()

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT配置
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class User(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register")
async def register(user: User):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # 检查用户名是否已存在
            cursor.execute("SELECT * FROM user_base_info WHERE username = %s", (user.username,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="用户名已存在")

            # 检查邮箱是否已存在
            cursor.execute("SELECT * FROM user_base_info WHERE email = %s", (user.email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="邮箱已被注册")

            # 对密码进行哈希处理
            hashed_password = pwd_context.hash(user.password)

            # 插入新用户
            cursor.execute(
                "INSERT INTO user_base_info (username, email, password_hash) VALUES (%s, %s, %s)",
                (user.username, user.email, hashed_password)
            )
            conn.commit()
            return {"message": "注册成功"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"数据库错误: {err}")
        finally:
            cursor.close()
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 查询用户信息
        cursor.execute("SELECT * FROM user_base_info WHERE username = %s", (form_data.username,))
        user = cursor.fetchone()

        if not user or not pwd_context.verify(form_data.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 生成JWT Token
        access_token = {"sub": user["username"]}
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        cursor.close()
        conn.close()

@router.get("/check")
async def check_login_status(request: Request):
    # 从请求头中获取token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return {"is_authenticated": False}

    token = auth_header.split(" ")[1]
    
    # 验证token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM user_base_info WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user:
                return {
                    "is_authenticated": True,
                    "user": {
                        "username": user["username"],
                        "avatar": user.get("avatar", "/images/default-avatar.png")
                    }
                }
        finally:
            cursor.close()
            conn.close()
    except jwt.PyJWTError:
        pass
    
    return {"is_authenticated": False}

@router.post("/reset-password")
async def reset_password(request: Request):
    try:
        data = await request.json()
        email = data.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="邮箱不能为空")
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # 检查邮箱是否存在
            cursor.execute("SELECT * FROM user_base_info WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="邮箱未注册")
            
            # 生成重置令牌（简化版，实际应使用更安全的方式）
            # 生成重置链接（实际项目应通过邮件发送）
            reset_token = jwt.encode(
                {
                    "sub": user["username"],
                    "exp": datetime.utcnow() + timedelta(hours=1),
                    "purpose": "password_reset"
                },
                SECRET_KEY,
                algorithm=ALGORITHM
            )
            
            reset_url = f"https://example.com/reset-password?token={reset_token}"
            
            # 实际项目这里应发送邮件
            print(f"密码重置链接: {reset_url}")  # 仅用于开发测试
            
            return {
                "message": "密码重置链接已发送至您的邮箱",
                "dev_note": "实际项目中链接应通过邮件发送"
            }
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"数据库错误: {err}")
        finally:
            cursor.close()
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")