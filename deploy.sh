#!/bin/bash
# 自动部署脚本 - 老王出品

set -e  # 遇到错误立即退出

echo "=========================================="
echo "       开始自动部署 - Auto Info"
echo "=========================================="
echo ""

# 1. 拉取最新代码
echo "📥 [1/3] 拉取最新代码..."
git pull
echo "✅ 代码更新完成"
echo ""

# 2. 拉取最新镜像
echo "🐳 [2/3] 拉取最新 Docker 镜像..."
docker compose pull
echo "✅ 镜像拉取完成"
echo ""

# 3. 启动服务
echo "🚀 [3/3] 启动服务..."
docker compose up -d
echo "✅ 服务启动完成"
echo ""

echo "=========================================="
echo "       部署完成！服务正在运行中"
echo "=========================================="
echo ""
echo "前端地址: http://localhost:5668"
echo "后端地址: http://localhost:5768"
echo ""
echo "查看日志: docker compose logs -f"
