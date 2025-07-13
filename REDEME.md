# HTML代理系统部署流程

## 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker构建流程                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   源代码仓库     │    │   Docker构建     │    │   容器运行       │
│                │    │                │    │                │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ front/      │ │───▶│ │前端构建阶段  │ │───▶│ │ nginx容器   │ │
│ │ - Vue3项目  │ │    │ │- npm build  │ │    │ │- 静态文件    │ │
│ │ - TypeScript│ │    │ │- 生成dist/  │ │    │ │- 反向代理    │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ │- 端口8080   │ │
│                │    │                │    │ └─────────────┘ │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │                │
│ │ backend/    │ │───▶│ │后端构建阶段  │ │───▶│ ┌─────────────┐ │
│ │ - FastAPI   │ │    │ │- pip install│ │    │ │backend容器  │ │
│ │ - Python    │ │    │ │- 安装依赖    │ │    │ │- FastAPI    │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ │- 端口40000  │ │
│                │    │                │    │ └─────────────┘ │
│ ┌─────────────┐ │    │                │    │                │
│ │配置文件      │ │───▶│                │───▶│ ┌─────────────┐ │
│ │- nginx.conf │ │    │                │    │ │共享存储      │ │
│ │- Dockerfile │ │    │                │    │ │- ./data     │ │
│ │- compose.yml│ │    │                │    │ │- ./uploads  │ │
│ └─────────────┘ │    │                │    │ │- ./html_files│ │
└─────────────────┘    └─────────────────┘    │ └─────────────┘ │
                                              └─────────────────┘
```

## 网络架构

```
                    ┌─────────────────────────────────────┐
                    │             用户访问                 │
                    │        http://localhost:8080        │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │           Nginx容器                  │
                    │         (端口 8080:80)              │
                    │                                    │
                    │ ┌────────────┐  ┌────────────────┐ │
                    │ │  静态文件   │  │   API代理       │ │
                    │ │     /      │  │   /api/*       │ │
                    │ │  Vue前端   │  │      │         │ │
                    │ └────────────┘  └──────┼─────────┘ │
                    └─────────────────────────┼───────────┘
                                             │
                              Docker网络通信  │
                                             │
                    ┌─────────────────────────▼───────────┐
                    │         Backend容器                 │
                    │        (端口 40000)                │
                    │                                    │
                    │ ┌────────────────────────────────┐ │
                    │ │          FastAPI              │ │
                    │ │        - 用户认证API           │ │
                    │ │        - 文件上传API           │ │
                    │ │        - HTML文件服务          │ │
                    │ └────────────────────────────────┘ │
                    └─────────────────────────────────────┘
```

## 部署步骤

### 1. 环境准备
```bash
# 确保安装Docker和Docker Compose
docker --version
docker-compose --version

# 克隆项目
git clone <your-repo>
cd HTMLproxy
```

### 2. 构建和启动
```bash
# 一键构建并启动所有服务
docker-compose up --build

# 后台运行
docker-compose up --build -d
```

### 3. 验证部署
```bash
# 检查容器状态
docker-compose ps

# 查看日志
docker-compose logs nginx
docker-compose logs backend

# 测试访问
curl http://localhost:8080         # 前端
curl http://localhost:8080/api/    # 后端API
```

## 构建详细流程

### 阶段1: 前端构建 (frontend-build)
```dockerfile
FROM node:18 AS frontend-build
WORKDIR /app/front
COPY front/package*.json ./
RUN npm ci --legacy-peer-deps
COPY front/ .
ENV NODE_OPTIONS="--experimental-global-webcrypto"
RUN npm run build  # 生成 dist/ 目录
```

### 阶段2: 后端镜像 (backend)
```dockerfile
FROM python:3.10-slim AS backend
WORKDIR /app/backend
COPY backend/ .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/data /app/html_files /app/uploads
EXPOSE 40000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "40000"]
```

### 阶段3: Nginx镜像 (nginx)
```dockerfile
FROM nginx:stable-alpine AS nginx
COPY --from=frontend-build /app/front/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /app/data /app/html_files /app/uploads
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 服务配置

### Backend服务
- **目标**: `backend` (Dockerfile target)
- **端口**: 40000 (内部)
- **挂载卷**: 
  - `./data:/app/data`
  - `./html_files:/app/html_files`
  - `./uploads:/app/uploads`
- **环境变量**:
  - `HTML_DIR=/app/html_files`
  - `UPLOAD_DIR=/app/uploads`

### Nginx服务
- **目标**: `nginx` (Dockerfile target)
- **端口**: `8080:80` (外部访问)
- **依赖**: backend服务
- **挂载卷**: 与backend相同(共享数据)
- **配置**: 
  - 静态文件服务: `/`
  - API代理: `/api/*` → `backend:40000/api/*`
  - HTML文件: `/html/*` → `backend:40000/html/*`

## 开发环境

### 前端开发
```bash
cd front
npm install
npm run dev     # 开发服务器 (通常3000端口)
npm run build   # 构建生产版本
```

### 后端开发
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 40000
```

## 生产部署注意事项

1. **端口配置**
   - 开发: 前端3000, 后端40000
   - Docker: 统一通过8080访问
   - 生产: 可配置域名+SSL

2. **数据持久化**
   - 所有上传文件和数据库通过volume挂载
   - 容器重启不会丢失数据

3. **网络安全**
   - 后端服务不直接暴露到外网
   - 通过Nginx反向代理访问
   - 支持配置SSL证书

4. **扩展性**
   - 可独立扩展前后端容器
   - 支持负载均衡配置
   - 数据库可分离为独立服务
