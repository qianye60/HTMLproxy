#!/bin/sh

# 确保必要的目录存在
mkdir -p /app/data /app/html_files /app/uploads

# 设置Python路径
export PYTHONPATH=/app/backend:$PYTHONPATH

# 启动FastAPI后端
cd /app/backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 40000 &

# 等待后端服务启动
sleep 3

# 启动Nginx
nginx -g "daemon off;" 