#!/bin/bash
set -e

echo "开始前端构建..."

# 检查Node.js版本
echo "Node.js版本: $(node --version)"
echo "npm版本: $(npm --version)"

# 安装依赖
echo "安装依赖..."
npm install

# 尝试构建
echo "开始构建..."
npm run build-only

echo "前端构建完成！" 