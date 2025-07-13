#!/bin/bash
# 启动FastAPI后端
cd /app/backend
uvicorn main:app --host 0.0.0.0 --port 40000 &
# 启动Nginx
nginx -g "daemon off;" 