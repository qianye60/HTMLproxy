FROM python:3.10-slim

WORKDIR /app

# 复制requirements.txt并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 300 --retries 3 -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 复制后端代码
COPY . .

# 创建必要的目录
RUN mkdir -p /app/data /app/html_files /app/uploads

# 暴露端口
EXPOSE 40000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "40000"]