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
    
    # 关联文件
    files: List["File"] = Relationship(back_populates="user")

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