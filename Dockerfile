# 前端构建阶段
FROM node:18 AS frontend-build
WORKDIR /app/front
COPY front/package*.json ./
RUN npm ci --legacy-peer-deps
COPY front/ .
# 设置环境变量以解决crypto兼容性问题
ENV NODE_OPTIONS="--experimental-global-webcrypto"
RUN npm run build

# 后端镜像
FROM python:3.10-slim AS backend
WORKDIR /app/backend
COPY backend/ .
RUN pip install --no-cache-dir -r requirements.txt

# 创建必要的目录
RUN mkdir -p /app/data /app/html_files /app/uploads

EXPOSE 40000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "40000"]

# Nginx镜像
FROM nginx:stable-alpine AS nginx

# 拷贝前端静态资源
COPY --from=frontend-build /app/front/dist /usr/share/nginx/html

# 拷贝nginx配置
COPY nginx.conf /etc/nginx/nginx.conf

# 创建必要的目录
RUN mkdir -p /app/data /app/html_files /app/uploads

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 