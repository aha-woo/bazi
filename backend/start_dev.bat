@echo off
REM Windows开发环境启动脚本

echo 启动八字API开发服务器...

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
echo 检查依赖...
pip install -r requirements.txt -q

REM 检查.env文件
if not exist ".env" (
    echo 警告：.env文件不存在，使用默认配置
    echo 请复制env.example为.env并修改配置
)

REM 启动服务
echo 启动服务...
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause

