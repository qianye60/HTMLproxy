#!/bin/bash

# HTMLproxy 部署脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 显示帮助信息
show_help() {
    echo "HTMLproxy 部署脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help          显示此帮助信息"
    echo "  -m, --mode MODE     部署模式: dev (本地构建) 或 prod (预构建镜像)"
    echo "  -t, --tag TAG       镜像标签 (仅适用于prod模式)"
    echo "  -u, --update        更新现有部署"
    echo "  -s, --stop          停止服务"
    echo ""
    echo "示例:"
    echo "  $0 -m dev           # 开发模式部署"
    echo "  $0 -m prod          # 生产模式部署 (使用latest标签)"
    echo "  $0 -m prod -t 20241213-143022  # 使用特定标签部署"
    echo "  $0 -u               # 更新部署"
    echo "  $0 -s               # 停止服务"
}

# 默认参数
MODE="prod"
TAG="latest"
UPDATE=false
STOP=false

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -m|--mode)
            MODE="$2"
            shift 2
            ;;
        -t|--tag)
            TAG="$2"
            shift 2
            ;;
        -u|--update)
            UPDATE=true
            shift
            ;;
        -s|--stop)
            STOP=true
            shift
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker未安装${NC}"
    exit 1
fi

# 检查docker-compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误: docker-compose未安装${NC}"
    exit 1
fi

# 停止服务
if [ "$STOP" = true ]; then
    echo -e "${YELLOW}停止HTMLproxy服务...${NC}"
    docker-compose -f docker-compose.yml down 2>/dev/null || true
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
    echo -e "${GREEN}服务已停止${NC}"
    exit 0
fi

# 确定使用的compose文件
if [ "$MODE" = "dev" ]; then
    COMPOSE_FILE="docker-compose.yml"
    echo -e "${YELLOW}使用开发模式 (本地构建)${NC}"
elif [ "$MODE" = "prod" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    echo -e "${YELLOW}使用生产模式 (预构建镜像: qianye60/htmlproxy:$TAG)${NC}"
    
    # 如果指定了特定标签，修改compose文件
    if [ "$TAG" != "latest" ]; then
        sed "s/:latest/:$TAG/g" docker-compose.prod.yml > docker-compose.prod.tmp.yml
        COMPOSE_FILE="docker-compose.prod.tmp.yml"
    fi
else
    echo -e "${RED}错误: 无效的模式 '$MODE'。支持的模式: dev, prod${NC}"
    exit 1
fi

# 检查compose文件是否存在
if [ ! -f "$COMPOSE_FILE" ]; then
    echo -e "${RED}错误: 找不到 $COMPOSE_FILE${NC}"
    exit 1
fi

# 创建必要的目录
echo -e "${YELLOW}创建必要的目录...${NC}"
mkdir -p data html_files uploads

# 更新模式
if [ "$UPDATE" = true ]; then
    echo -e "${YELLOW}更新HTMLproxy部署...${NC}"
    
    if [ "$MODE" = "prod" ]; then
        echo -e "${YELLOW}拉取最新镜像...${NC}"
        docker-compose -f "$COMPOSE_FILE" pull
    fi
    
    echo -e "${YELLOW}重启服务...${NC}"
    docker-compose -f "$COMPOSE_FILE" up -d
else
    # 停止可能存在的旧服务
    echo -e "${YELLOW}停止现有服务...${NC}"
    docker-compose -f docker-compose.yml down 2>/dev/null || true
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
    
    # 启动新服务
    echo -e "${YELLOW}启动HTMLproxy服务...${NC}"
    if [ "$MODE" = "dev" ]; then
        docker-compose -f "$COMPOSE_FILE" up -d --build
    else
        docker-compose -f "$COMPOSE_FILE" up -d
    fi
fi

# 清理临时文件
if [ -f "docker-compose.prod.tmp.yml" ]; then
    rm docker-compose.prod.tmp.yml
fi

# 等待服务启动
echo -e "${YELLOW}等待服务启动...${NC}"
sleep 5

# 检查服务状态
if docker-compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
    echo -e "${GREEN}✓ HTMLproxy服务启动成功!${NC}"
    echo -e "${GREEN}访问地址: http://localhost:8080${NC}"
    echo ""
    echo "查看日志: docker-compose -f $COMPOSE_FILE logs -f"
    echo "停止服务: $0 -s"
else
    echo -e "${RED}✗ 服务启动失败${NC}"
    echo "查看日志: docker-compose -f $COMPOSE_FILE logs"
    exit 1
fi