# 前端构建阶段
FROM node:20-alpine AS frontend-build
WORKDIR /app/front
COPY front/package*.json ./
RUN npm ci --legacy-peer-deps
COPY front/ .
RUN npm run build

# 后端构建阶段
FROM python:3.10-alpine AS backend-build
WORKDIR /app/backend
COPY backend/ .
RUN pip install --no-cache-dir -r requirements.txt

# 生产镜像
FROM nginx:1.25
WORKDIR /app

# 拷贝前端静态资源
COPY --from=frontend-build /app/front/dist /app/front/dist

# 拷贝nginx配置
COPY nginx.conf /etc/nginx/nginx.conf

# 拷贝后端
COPY --from=backend-build /app/backend /app/backend

# 创建必要的目录
RUN mkdir -p /app/data /app/html_files /app/uploads

# 启动脚本
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80

CMD ["/bin/bash", "/start.sh"] 