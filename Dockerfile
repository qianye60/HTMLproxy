# 前端构建阶段
FROM node:18 AS frontend-build
WORKDIR /app/front
COPY front/package*.json ./
RUN npm ci --legacy-peer-deps
COPY front/ .
# 设置环境变量以解决crypto兼容性问题
ENV NODE_OPTIONS="--experimental-global-webcrypto"
RUN npm run build

# 后端构建阶段
FROM python:3.10-slim AS backend-build
WORKDIR /app/backend
COPY backend/ .
RUN pip install --no-cache-dir -r requirements.txt

# Nginx镜像
FROM nginx:stable-alpine AS nginx
# 安装bash和python
RUN apk add --no-cache bash python3 py3-pip

# 拷贝前端静态资源
COPY --from=frontend-build /app/front/dist /usr/share/nginx/html

# 拷贝后端代码和依赖
COPY --from=backend-build /app/backend /app/backend

# 拷贝nginx配置
COPY nginx.conf /etc/nginx/nginx.conf

# 创建必要的目录
RUN mkdir -p /app/data /app/html_files /app/uploads

# 启动脚本
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80

CMD ["/bin/sh", "/start.sh"] 