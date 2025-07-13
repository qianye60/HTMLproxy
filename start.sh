#!/bin/sh

# 确保必要的目录存在
mkdir -p /app/data /app/html_files /app/uploads

# 启动FastAPI后端
cd /app/backend
uvicorn main:app --host 0.0.0.0 --port 40000 &

# 启动Nginx
nginx -g "daemon off;" 