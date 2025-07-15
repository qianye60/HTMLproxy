# 构建阶段
FROM node:18 AS builder

WORKDIR /app

# 复制package文件
COPY package*.json ./

# 安装依赖
RUN npm ci --legacy-peer-deps

# 复制源代码
COPY . .

# 设置环境变量
ENV NODE_OPTIONS="--experimental-global-webcrypto"

# 构建前端
RUN npm run build

# 生产阶段
FROM nginx:stable-alpine

# 复制构建结果到nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制nginx配置（如果需要自定义配置）
COPY ../nginx.conf /etc/nginx/nginx.conf

# 暴露端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]