#需求包或模块
import uvicorn
from fastapi.middleware.cors import CORSMiddleware #跨域访问请求配置
from fastapi import FastAPI #类型注解

#引入子级API
from user.user import user as user_router
from upfile.upfile import upfile as upfile_router
from database import create_db_and_tables
import os
from fastapi.responses import FileResponse
from fastapi import HTTPException

app = FastAPI()#网站上线需要增加参数关闭测试文档 docs_url=None, redoc_url=None,openapi_url=None

# 在应用启动时初始化数据库
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 注册路由
app.include_router(user_router, prefix='/api', tags=['用户认证'])
app.include_router(upfile_router, prefix='/api', tags=['文件管理'])

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # 允许的源
    allow_credentials=True,  # 如果需要支持 cookies，设置为 True
    allow_methods=["*"],      # 允许所有方法 ("GET", "POST", "PUT", etc.)
    allow_headers=["*"],      # 允许所有头
)

@app.get("/")
async def root():
    return "Hello!"

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=40000)
    

