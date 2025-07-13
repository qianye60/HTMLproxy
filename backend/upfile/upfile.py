import os
import uuid
import shutil
from datetime import datetime
from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from database import get_session, File, User
from user.user import get_user_by_username, oauth2_scheme
from jwt import decode
from user.user import SECRET_KEY, ALGORITHM
from pydantic import BaseModel

# 创建路由器
upfile = APIRouter()

# 文件存储配置
UPLOAD_DIR = "uploads"
HTML_DIR = "html_files"

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(HTML_DIR, exist_ok=True)

def get_user_upload_dir(username: str) -> str:
    """获取用户上传目录"""
    user_dir = os.path.join(HTML_DIR, username)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

# 请求模型
class ProjectNameUpdate(BaseModel):
    """项目名更新请求模型"""
    project_name: str

# 统计响应模型
class StatCard(BaseModel):
    """统计卡片模型"""
    id: str
    label: str
    value: str | int
    color: str
    iconColor: str
    icon: str

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    """获取当前用户"""
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]
        user = get_user_by_username(username, session)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="无效的令牌")

def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes // 1024}KB"
    else:
        return f"{size_bytes // (1024 * 1024)}MB"

def generate_access_url(username: str, filename: str) -> str:
    """生成访问URL"""
    return f"/html/{username}/{filename}"

# API路由
@upfile.post("/upload")
async def upload_file(
    file: UploadFile,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """上传HTML文件"""
    # 检查文件类型
    if not file.filename.lower().endswith(('.html', '.htm')):
        raise HTTPException(status_code=400, detail="只支持HTML文件")
    
    # 获取用户上传目录
    user_upload_dir = get_user_upload_dir(current_user.username)
    
    # 生成唯一文件名
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(user_upload_dir, unique_filename)
    
    try:
        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 获取文件大小
        file_size = os.path.getsize(file_path)
        
        # 创建文件记录
        db_file = File(
            user_id=current_user.id,
            project_name="未命名项目",
            filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            access_url=generate_access_url(current_user.username, unique_filename)
        )
        
        session.add(db_file)
        session.commit()
        session.refresh(db_file)
        
        return {
            "id": db_file.id,
            "project_name": db_file.project_name,
            "filename": db_file.filename,
            "url": db_file.access_url,
            "size": format_file_size(db_file.file_size),
            "upload_time": db_file.upload_time.isoformat()
        }
        
    except Exception as e:
        # 如果保存失败，删除已创建的文件
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@upfile.get("/files")
async def get_files(
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """获取用户文件列表"""
    statement = select(File).where(File.user_id == current_user.id).order_by(File.upload_time.desc())
    files = session.exec(statement).all()
    
    return [
        {
            "id": file.id,
            "project_name": file.project_name,
            "filename": file.filename,
            "url": file.access_url,
            "size": format_file_size(file.file_size),
            "upload_time": file.upload_time.isoformat()
        }
        for file in files
    ]

@upfile.patch("/files/{file_id}")
async def update_project_name(
    file_id: int,
    update_data: ProjectNameUpdate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """更新项目名称"""
    statement = select(File).where(File.id == file_id, File.user_id == current_user.id)
    file = session.exec(statement).first()
    
    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    file.project_name = update_data.project_name
    session.add(file)
    session.commit()
    
    return {"success": True}

@upfile.delete("/files/{file_id}")
async def delete_file(
    file_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """删除文件"""
    statement = select(File).where(File.id == file_id, File.user_id == current_user.id)
    file = session.exec(statement).first()
    
    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    # 删除物理文件
    if os.path.exists(file.file_path):
        os.remove(file.file_path)
    
    # 删除数据库记录
    session.delete(file)
    session.commit()
    
    return {"success": True}

@upfile.get("/stats")
async def get_stats(
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """获取用户统计数据"""
    # 获取文件总数
    statement = select(File).where(File.user_id == current_user.id)
    files = session.exec(statement).all()
    total_files = len(files)
    
    # 计算总文件大小
    total_size = sum(file.file_size for file in files)
    
    return [
        {
            "id": "total-files",
            "label": "文件总数",
            "value": total_files,
            "color": "#dbeafe",
            "iconColor": "#3b82f6",
            "icon": "FileIcon"
        },
        {
            "id": "remaining-space",
            "label": "已用空间",
            "value": f"{format_file_size(total_size)}/50MB",
            "color": "#dcfce7",
            "iconColor": "#10b981",
            "icon": "StorageIcon"
        }
    ]

@upfile.get("/html/{username}/{filename}")
async def serve_html_file(username: str, filename: str):
    """提供HTML文件访问"""
    file_path = os.path.join(HTML_DIR, username, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        path=file_path,
        media_type="text/html"
        # 不加 filename 参数，避免浏览器下载
    ) 