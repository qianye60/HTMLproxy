# 用户认证和授权模块
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated, List
from database import get_session, User, File
from fastapi import APIRouter, HTTPException, Depends, Header, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlmodel import Field, Session, SQLModel, select, create_engine, Relationship
from jwt import decode, encode
from pydantic import BaseModel

# 使用环境变量获取密钥，避免写死在代码中，生产环境请务必设置 SECRET_KEY 环境变量
import os
SECRET_KEY = secrets.token_hex(32)

# 创建路由器
user = APIRouter()

# 配置参数
ACCESS_TOKEN_EXPIRE_DAYS = 7  # 访问令牌过期天数
# 使用固定的密钥，避免每次重启都重新生成
ALGORITHM = "HS256"  # 加密算法

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# OAuth2密码Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 密码验证函数
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """获取密码哈希值"""
    return pwd_context.hash(password)

def create_access_token(data: dict):
    """创建访问令牌"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    return encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

# 请求模型
class LoginRequest(BaseModel):
    """登录请求模型"""
    email: str
    password: str

class RegisterRequest(BaseModel):
    """注册请求模型"""
    username: str
    email: str
    password: str

# 响应模型
class UserInfo(BaseModel):
    """用户信息响应模型"""
    username: str
    email: str
    avatar: str = ""
    is_admin: bool = False

class FileResponse(BaseModel):
    """文件响应模型"""
    id: int
    project_name: str
    filename: str
    url: str
    size: str
    upload_time: str

def get_user(email: str, session: Session):
    """根据邮箱获取用户"""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def get_user_by_username(username: str, session: Session):
    """根据用户名获取用户"""
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

# API路由
@user.post("/login")
async def login(request: LoginRequest, session: Session = Depends(get_session)):
    """用户登录"""
    user_db = get_user(request.email, session)

    if not user_db:
        raise HTTPException(status_code=401, detail="用户不存在")
    
    if not verify_password(request.password, user_db.hashed_password):
        raise HTTPException(status_code=401, detail="密码错误")
    
    return {"access_token": create_access_token(data={"sub": user_db.username}), "token_type": "Bearer"}

@user.post("/register")
async def register(request: RegisterRequest, session: Session = Depends(get_session)):
    """用户注册"""
    import re
    
    # 邮箱格式验证
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.match(email_pattern, request.email):
        raise HTTPException(status_code=400, detail="邮箱格式无效")
    
    # 检查邮箱是否已存在
    if get_user(request.email, session):
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    # 检查用户名是否已存在
    statement = select(User).where(User.username == request.username)
    if session.exec(statement).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查是否是第一个用户，如果是则设置为管理员
    user_count = session.exec(select(User)).all()
    is_first_user = len(user_count) == 0
    
    # 创建新用户
    new_user = User(
        username=request.username, 
        email=request.email, 
        hashed_password=get_password_hash(request.password),
        is_admin=is_first_user  # 第一个用户为管理员
    )
    session.add(new_user)
    session.commit()
    
    return {"access_token": create_access_token(data={"sub": new_user.username}), "token_type": "Bearer"}

@user.post("/verify")
async def verify_token(authorization: str = Header(None), session: Session = Depends(get_session)):
    """验证用户令牌"""
    
    # 从Authorization头获取token
    if not authorization or not authorization.startswith("Bearer "):
        return {"islogin": False, "userauth": False}
    
    token = authorization.replace("Bearer ", "")
    
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]
        user_db = get_user_by_username(username, session)
        if user_db:
            return {"islogin": True, "userauth": True, "username": username}
        else:
            return {"islogin": False, "userauth": False}
    except InvalidTokenError as e:
        print(f"令牌验证失败: {str(e)}")
        return {"islogin": False, "userauth": False}
    except Exception as e:
        print(f"获取用户时出错: {str(e)}")
        return {"islogin": False, "userauth": False}

@user.get("/user/info")
async def get_user_info(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    """获取用户信息"""
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]
        user_db = get_user_by_username(username, session)
        
        if not user_db:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        return UserInfo(
            username=user_db.username,
            email=user_db.email,
            avatar="",
            is_admin=user_db.is_admin
        )
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的令牌")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户信息失败: {str(e)}")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user_by_username(username, session)
    if user is None:
        raise credentials_exception
    
    return user 