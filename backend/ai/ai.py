from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select, func
from database import SessionDep, User, AIGeneration, APIConfig, SystemConfig
from user.user import get_current_user
from datetime import datetime, date
from typing import List, Optional
import requests
import re
import json
from pydantic import BaseModel

ai = APIRouter()

# 请求模型
class AIGenerateRequest(BaseModel):
    prompt: str

class APIConfigCreate(BaseModel):
    name: str
    api_key: str
    base_url: str
    model: str

class APIConfigUpdate(BaseModel):
    name: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None
    is_active: Optional[bool] = None

class SystemConfigRequest(BaseModel):
    key: str
    value: str
    description: Optional[str] = None

# 响应模型
class AIGenerateResponse(BaseModel):
    content: str
    remaining_uses: int

class UsageStatsResponse(BaseModel):
    used_today: int
    remaining_today: int
    total_limit: int

def clean_html_response(response_text: str) -> str:
    """清理AI响应，提取纯HTML内容"""
    # 移除markdown代码块标记
    cleaned = re.sub(r'^```html\s*\n?', '', response_text, flags=re.MULTILINE)
    cleaned = re.sub(r'\n?```$', '', cleaned, flags=re.MULTILINE)
    
    # 移除多余的说明文字（常见的AI回复模式）
    cleaned = re.sub(r'^(这是|这里是|以下是).*?HTML.*?[：:]?\s*\n?', '', cleaned, flags=re.MULTILINE | re.IGNORECASE)
    cleaned = re.sub(r'^根据.*?要求.*?[：:]?\s*\n?', '', cleaned, flags=re.MULTILINE | re.IGNORECASE)
    
    # 移除开头和结尾的空白
    cleaned = cleaned.strip()
    
    # 如果内容不以<!DOCTYPE或<html开始，且包含HTML标签，尝试包装
    if not cleaned.startswith(('<!DOCTYPE', '<html')) and '<' in cleaned and '>' in cleaned:
        # 检查是否已经有完整的html结构
        if not ('<html' in cleaned.lower() and '</html>' in cleaned.lower()):
            cleaned = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Page</title>
</head>
<body>
{cleaned}
</body>
</html>"""
    
    return cleaned

def get_daily_usage_count(session: Session, user_id: int) -> int:
    """获取用户今日使用次数"""
    today = date.today()
    
    # 查询今日使用次数
    count = session.exec(
        select(func.count(AIGeneration.id))
        .where(AIGeneration.user_id == user_id)
        .where(func.date(AIGeneration.generation_time) == today)
    ).first()
    
    return count or 0

def get_daily_limit(session: Session) -> int:
    """获取每日使用限制"""
    config = session.exec(
        select(SystemConfig)
        .where(SystemConfig.key == "daily_ai_limit")
    ).first()
    
    if config:
        try:
            return int(config.value)
        except ValueError:
            return 10  # 默认值
    
    # 如果没有配置，创建默认配置
    default_config = SystemConfig(
        key="daily_ai_limit",
        value="10",
        description="每日AI生成次数限制"
    )
    session.add(default_config)
    session.commit()
    
    return 10

def get_active_api_config(session: Session) -> Optional[APIConfig]:
    """获取活跃的API配置"""
    config = session.exec(
        select(APIConfig)
        .where(APIConfig.is_active == True)
        .order_by(APIConfig.updated_time.desc())
    ).first()
    
    return config

@ai.post("/generate", response_model=AIGenerateResponse)
async def generate_html(
    request: AIGenerateRequest,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    """AI生成HTML网站"""
    # 获取每日限制
    daily_limit = get_daily_limit(session)
    used_today = get_daily_usage_count(session, current_user.id)
    
    if used_today >= daily_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="今日生成次数已用完，请明天再试"
        )
    
    # 获取API配置
    api_config = get_active_api_config(session)
    if not api_config:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="暂无可用的API配置，请联系管理员"
        )
    
    # 构建提示词
    system_prompt = """你是一个专业的前端开发专家。请根据用户的需求生成完整的HTML网页代码。

要求：
1. 生成完整的HTML5页面，包含DOCTYPE、html、head、body标签
2. 包含必要的meta标签和响应式设计
3. 内联CSS样式，不使用外部样式文件
4. 代码规范整洁，注重用户体验
5. 响应式设计，适配移动端
6. 只返回HTML代码，不要任何解释文字"""

    try:
        # 调用AI API
        headers = {
            "Authorization": f"Bearer {api_config.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": api_config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        response = requests.post(
            f"{api_config.base_url}/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"AI服务调用失败: {response.status_code}"
            )
        
        result = response.json()
        
        if 'choices' not in result or not result['choices']:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI服务返回格式异常"
            )
        
        generated_content = result['choices'][0]['message']['content']
        
        # 清理生成的内容
        cleaned_content = clean_html_response(generated_content)
        
        # 保存生成记录
        ai_generation = AIGeneration(
            user_id=current_user.id,
            prompt=request.prompt,
            generated_content=cleaned_content
        )
        session.add(ai_generation)
        session.commit()
        
        # 计算剩余次数
        remaining_uses = daily_limit - (used_today + 1)
        
        return AIGenerateResponse(
            content=cleaned_content,
            remaining_uses=remaining_uses
        )
        
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"网络请求失败: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成失败: {str(e)}"
        )

@ai.get("/usage", response_model=UsageStatsResponse)
async def get_usage_stats(
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    """获取用户使用统计"""
    daily_limit = get_daily_limit(session)
    used_today = get_daily_usage_count(session, current_user.id)
    remaining_today = max(0, daily_limit - used_today)
    
    return UsageStatsResponse(
        used_today=used_today,
        remaining_today=remaining_today,
        total_limit=daily_limit
    )

@ai.get("/history/{item_id}")
async def get_generation_item(
    item_id: int,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    """获取单个生成记录详情"""
    item = session.exec(
        select(AIGeneration)
        .where(AIGeneration.id == item_id)
        .where(AIGeneration.user_id == current_user.id)
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="记录不存在"
        )
    
    return {
        "id": item.id,
        "prompt": item.prompt,
        "generated_content": item.generated_content,
        "generation_time": item.generation_time
    }

@ai.get("/history")
async def get_generation_history(
    session: SessionDep,
    current_user: User = Depends(get_current_user),
    limit: int = 20
):
    """获取生成历史"""
    history = session.exec(
        select(AIGeneration)
        .where(AIGeneration.user_id == current_user.id)
        .order_by(AIGeneration.generation_time.desc())
        .limit(limit)
    ).all()
    
    return [
        {
            "id": item.id,
            "prompt": item.prompt,
            "generation_time": item.generation_time,
            "content_preview": item.generated_content[:200] + "..." if len(item.generated_content) > 200 else item.generated_content
        }
        for item in history
    ]

# 管理员API
def verify_admin(current_user: User = Depends(get_current_user)):
    """验证管理员权限"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user

@ai.get("/admin/api-configs")
async def get_api_configs(
    session: SessionDep,
    admin_user: User = Depends(verify_admin)
):
    """获取API配置列表"""
    configs = session.exec(select(APIConfig).order_by(APIConfig.created_time.desc())).all()
    return [
        {
            "id": config.id,
            "name": config.name,
            "base_url": config.base_url,
            "model": config.model,
            "is_active": config.is_active,
            "created_time": config.created_time,
            "api_key": config.api_key[:10] + "..." if config.api_key else None  # 隐藏敏感信息
        }
        for config in configs
    ]

@ai.post("/admin/api-configs")
async def create_api_config(
    request: APIConfigCreate,
    session: SessionDep,
    admin_user: User = Depends(verify_admin)
):
    """创建API配置"""
    config = APIConfig(**request.dict())
    session.add(config)
    session.commit()
    session.refresh(config)
    
    return {"message": "API配置创建成功", "id": config.id}

@ai.put("/admin/api-configs/{config_id}")
async def update_api_config(
    config_id: int,
    request: APIConfigUpdate,
    session: SessionDep,
    admin_user: User = Depends(verify_admin)
):
    """更新API配置"""
    config = session.get(APIConfig, config_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API配置不存在"
        )
    
    # 更新字段
    for field, value in request.dict(exclude_unset=True).items():
        setattr(config, field, value)
    
    config.updated_time = datetime.now()
    session.commit()
    
    return {"message": "API配置更新成功"}

@ai.delete("/admin/api-configs/{config_id}")
async def delete_api_config(
    config_id: int,
    session: SessionDep,
    admin_user: User = Depends(verify_admin)
):
    """删除API配置"""
    config = session.get(APIConfig, config_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API配置不存在"
        )
    
    session.delete(config)
    session.commit()
    
    return {"message": "API配置删除成功"}

@ai.get("/admin/usage-stats")
async def get_admin_usage_stats(
    session: SessionDep,
    admin_user: User = Depends(verify_admin)
):
    """获取全站使用统计"""
    today = date.today()
    
    # 今日总使用次数
    total_today = session.exec(
        select(func.count(AIGeneration.id))
        .where(func.date(AIGeneration.generation_time) == today)
    ).first() or 0
    
    # 今日活跃用户数
    active_users_today = session.exec(
        select(func.count(func.distinct(AIGeneration.user_id)))
        .where(func.date(AIGeneration.generation_time) == today)
    ).first() or 0
    
    return {
        "total_generations_today": total_today,
        "active_users_today": active_users_today,
        "total_users": session.exec(select(func.count(User.id))).first() or 0,
        "current_daily_limit": get_daily_limit(session)
    }

@ai.get("/admin/system-configs")
async def get_system_configs(
    session: SessionDep,
    admin_user: User = Depends(verify_admin)
):
    """获取系统配置列表"""
    configs = session.exec(select(SystemConfig)).all()
    return [
        {
            "id": config.id,
            "key": config.key,
            "value": config.value,
            "description": config.description,
            "updated_time": config.updated_time
        }
        for config in configs
    ]

@ai.put("/admin/system-config/{config_key}")
async def update_system_config(
    config_key: str,
    request: SystemConfigRequest,
    session: SessionDep,
    admin_user: User = Depends(verify_admin)
):
    """更新系统配置"""
    config = session.exec(
        select(SystemConfig).where(SystemConfig.key == config_key)
    ).first()
    
    if not config:
        # 创建新配置
        config = SystemConfig(
            key=request.key,
            value=request.value,
            description=request.description
        )
        session.add(config)
    else:
        # 更新现有配置
        config.value = request.value
        if request.description:
            config.description = request.description
        config.updated_time = datetime.now()
    
    session.commit()
    session.refresh(config)
    
    return {"message": "配置更新成功", "config": {
        "key": config.key,
        "value": config.value,
        "description": config.description
    }}

@ai.put("/admin/daily-limit")
async def update_daily_limit(
    limit: int,
    session: SessionDep,
    admin_user: User = Depends(verify_admin)
):
    """更新每日生成次数限制"""
    if limit < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="限制次数必须大于0"
        )
    
    config = session.exec(
        select(SystemConfig).where(SystemConfig.key == "daily_ai_limit")
    ).first()
    
    if not config:
        config = SystemConfig(
            key="daily_ai_limit",
            value=str(limit),
            description="每日AI生成次数限制"
        )
        session.add(config)
    else:
        config.value = str(limit)
        config.updated_time = datetime.now()
    
    session.commit()
    
    return {"message": f"每日限制已更新为 {limit} 次"}

@ai.get("/admin/daily-limit")
async def get_daily_limit_config(
    session: SessionDep,
    admin_user: User = Depends(verify_admin)
):
    """获取当前每日限制配置"""
    return {"daily_limit": get_daily_limit(session)}