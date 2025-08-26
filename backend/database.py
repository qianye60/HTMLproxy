import os
from sqlmodel import Session, SQLModel, create_engine, Field, Relationship
from typing import Annotated, List
from fastapi import Depends
from datetime import datetime

# 数据库配置
sqlite_file_name = "lxhtml.db"

# 使用环境变量或默认路径
data_dir = os.getenv("DATA_DIR", "/app/data")

# 确保数据目录存在
os.makedirs(data_dir, exist_ok=True)

# 数据库连接URL
sqlite_url = f"sqlite:///{os.path.join(data_dir, sqlite_file_name)}"

# 数据库连接参数
connect_args = {"check_same_thread": False}

# 创建数据库引擎
engine = create_engine(sqlite_url, connect_args=connect_args)

# 用户模型
class User(SQLModel, table=True):
    """用户数据模型"""
    id: int = Field(default=None, primary_key=True)
    username: str = Field(default=None)
    email: str = Field(default=None)
    hashed_password: str = Field(default=None)
    is_admin: bool = Field(default=False)  # 是否为超级管理员
    
    # 关联文件
    files: List["File"] = Relationship(back_populates="user")
    # 关联AI生成记录
    ai_generations: List["AIGeneration"] = Relationship(back_populates="user")

# 文件模型
class File(SQLModel, table=True):
    """文件数据模型"""
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    project_name: str = Field(default="未命名项目")
    filename: str = Field(default=None)
    file_path: str = Field(default=None)
    file_size: int = Field(default=0)
    upload_time: datetime = Field(default_factory=datetime.now)
    access_url: str = Field(default=None)
    
    # 关联用户
    user: User = Relationship(back_populates="files")

# 创建数据库和表
def create_db_and_tables():
    """创建数据库和所有表"""
    SQLModel.metadata.create_all(engine)

# 数据库会话依赖
def get_session():
    """获取数据库会话"""
    with Session(engine) as session:
        yield session

# 会话依赖类型注解
SessionDep = Annotated[Session, Depends(get_session)]

# AI生成记录模型
class AIGeneration(SQLModel, table=True):
    """AI生成记录数据模型"""
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    prompt: str = Field(default=None)  # 用户输入的提示词
    generated_content: str = Field(default=None)  # 生成的HTML内容
    generation_time: datetime = Field(default_factory=datetime.now)
    
    # 关联用户
    user: User = Relationship(back_populates="ai_generations")

# API配置模型  
class APIConfig(SQLModel, table=True):
    """API配置数据模型"""
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None)  # 模型名称
    api_key: str = Field(default=None)  # API密钥
    base_url: str = Field(default=None)  # API基础URL
    model: str = Field(default=None)  # 模型标识
    is_active: bool = Field(default=True)  # 是否启用
    created_time: datetime = Field(default_factory=datetime.now)
    updated_time: datetime = Field(default_factory=datetime.now)

# 系统配置模型
class SystemConfig(SQLModel, table=True):
    """系统配置数据模型"""
    id: int = Field(default=None, primary_key=True)
    key: str = Field(default=None, unique=True)  # 配置键
    value: str = Field(default=None)  # 配置值
    description: str = Field(default=None)  # 配置描述
    updated_time: datetime = Field(default_factory=datetime.now)