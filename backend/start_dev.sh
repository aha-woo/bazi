#!/bin/bash
# 开发环境启动脚本

echo "🚀 启动八字API开发服务器..."

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "检查依赖..."
pip install -r requirements.txt -q

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "警告：.env文件不存在，使用默认配置"
    echo "请复制env.example为.env并修改配置"
fi

# 启动服务
echo "启动服务..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

