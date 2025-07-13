# Docker部署指南

本项目支持两种Docker部署方式：

## 1. 本地构建部署

适用于开发环境和需要修改代码的场景：

```bash
# 使用默认的docker-compose.yml
docker-compose up -d --build
```

## 2. 预构建镜像部署（推荐）

适用于生产环境，直接使用GitHub Actions构建的镜像：

```bash
# 使用预构建镜像
docker-compose -f docker-compose.prod.yml up -d
```

### 使用指定版本标签

```bash
# 使用最新版本
docker-compose -f docker-compose.prod.yml up -d

# 使用特定时间戳版本
sed 's/:latest/:20241213-143022/g' docker-compose.prod.yml | docker-compose -f - up -d

# 使用特定commit版本
sed 's/:latest/:a1b2c3d/g' docker-compose.prod.yml | docker-compose -f - up -d
```

## 镜像标签说明

GitHub Actions会自动构建并推送以下标签的镜像到Docker Hub (`qianye60/htmlproxy`):

- `latest` - 最新的main分支构建
- `YYYYMMDD-HHMMSS` - 时间戳版本，如 `20241213-143022`
- `commit-hash` - Git提交哈希的前7位，如 `a1b2c3d`

## 环境变量

- `HTML_DIR` - HTML文件存储目录 (默认: `/app/html_files`)
- `UPLOAD_DIR` - 上传文件临时目录 (默认: `/app/uploads`)

## 数据持久化

以下目录通过volume映射实现数据持久化：
- `./data` - 数据库文件
- `./html_files` - 用户上传的HTML文件
- `./uploads` - 上传文件临时存储

## 端口映射

- 容器端口 `80` 映射到主机端口 `8080`
- 访问地址: http://localhost:8080

## 更新部署

```bash
# 拉取最新镜像
docker-compose -f docker-compose.prod.yml pull

# 重启服务
docker-compose -f docker-compose.prod.yml up -d
```