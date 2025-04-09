from datetime import datetime, timedelta
from jose import jwt
from pydantic import BaseModel

# JWT配置
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    创建JWT访问令牌。

    参数:
    - data: 包含用户信息的字典。
    - expires_delta: 令牌的有效期，默认为30分钟。

    返回:
    - str: 生成的JWT令牌。
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """
    验证并解码JWT访问令牌。

    参数:
    - token: 要验证的JWT令牌。

    返回:
    - dict: 解码后的令牌数据。

    异常:
    - jwt.JWTError: 如果令牌无效或已过期。
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

