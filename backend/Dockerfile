# 后端 Dockerfile - FastAPI + SQLite
# 老王出品，多阶段构建，镜像精简

# ========== 阶段1: Builder ==========
FROM python:3.11-slim AS builder

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# 先复制依赖文件，利用层缓存
COPY requirements.txt .

# 安装依赖到 /install 目录
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ========== 阶段2: Production ==========
FROM python:3.11-slim

# 只安装运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*

# 创建非 root 用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# 从 builder 阶段复制已安装的依赖
COPY --from=builder /install /usr/local

# 复制应用代码
COPY --chown=appuser:appuser ./app ./app

# 创建数据目录
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

# 切换到非 root 用户
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()"

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
