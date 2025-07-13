# 用户认证和授权模块
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated, List
from database import get_session, User, File
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlmodel import Field, Session, SQLModel, select, create_engine, Relationship
from jwt import decode, encode
from pydantic import BaseModel

# 创建路由器
user = APIRouter()

# 配置参数
ACCESS_TOKEN_EXPIRE_DAYS = 7  # 访问令牌过期天数
SECRET_KEY = secrets.token_hex(32)  # 密钥
ALGORITHM = "HS256"  # 加密算法

if not SECRET_KEY:
    raise ValueError("必须提供SECRET_KEY环境变量!")

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
    
    # 创建新用户
    new_user = User(
        username=request.username, 
        email=request.email, 
        hashed_password=get_password_hash(request.password)
    )
    session.add(new_user)
    session.commit()
    
    return {"access_token": create_access_token(data={"sub": new_user.username}), "token_type": "Bearer"}

@user.post("/verify")
async def verify_token(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    """验证用户令牌"""
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
            avatar=""
        )
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的令牌")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户信息失败: {str(e)}") 