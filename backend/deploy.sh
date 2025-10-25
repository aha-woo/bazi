#!/bin/bash
# 八字API部署脚本 - Ubuntu系统

set -e

echo "🚀 开始部署八字计算API..."

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查是否为root用户
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}警告：不建议使用root用户运行此脚本${NC}"
    read -p "是否继续? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 1. 更新系统
echo -e "${GREEN}[1/8] 更新系统...${NC}"
sudo apt update
sudo apt upgrade -y

# 2. 安装依赖
echo -e "${GREEN}[2/8] 安装系统依赖...${NC}"
echo "检测到的数据库服务："
if systemctl is-active --quiet mariadb; then
    echo -e "${GREEN}  ✓ MariaDB (运行中)${NC}"
    DB_SERVICE="mariadb"
elif systemctl is-active --quiet mysql; then
    echo -e "${GREEN}  ✓ MySQL (运行中)${NC}"
    DB_SERVICE="mysql"
else
    echo -e "${YELLOW}  ! 未检测到运行中的数据库服务${NC}"
    DB_SERVICE="none"
fi

echo ""
read -p "是否使用现有的数据库服务? (y/n) [y]: " USE_EXISTING_DB
USE_EXISTING_DB=${USE_EXISTING_DB:-y}

if [[ $USE_EXISTING_DB =~ ^[Yy]$ ]] && [[ $DB_SERVICE != "none" ]]; then
    echo -e "${GREEN}将使用现有的 ${DB_SERVICE} 服务${NC}"
    # 只安装Python和Nginx，不安装数据库
    sudo apt install -y python3 python3-pip python3-venv nginx
else
    echo -e "${YELLOW}将安装新的MySQL服务${NC}"
    sudo apt install -y python3 python3-pip python3-venv mysql-server nginx
    DB_SERVICE="mysql"
    # 启动MySQL
    sudo systemctl start mysql
    sudo systemctl enable mysql
fi

# 3. 配置数据库
echo -e "${GREEN}[3/8] 配置数据库...${NC}"
read -p "请输入数据库名称 [bazi_db]: " DB_NAME
DB_NAME=${DB_NAME:-bazi_db}

read -p "请输入数据库用户名 [bazi_user]: " DB_USER
DB_USER=${DB_USER:-bazi_user}

read -sp "请输入数据库密码: " DB_PASSWORD
echo

read -p "请输入数据库主机 [localhost]: " DB_HOST
DB_HOST=${DB_HOST:-localhost}

read -p "请输入数据库端口 [3306]: " DB_PORT
DB_PORT=${DB_PORT:-3306}

# 确保数据库服务运行
if ! systemctl is-active --quiet $DB_SERVICE; then
    echo -e "${YELLOW}启动 ${DB_SERVICE} 服务...${NC}"
    sudo systemctl start $DB_SERVICE
    sudo systemctl enable $DB_SERVICE
fi

# 创建数据库和用户
echo -e "${GREEN}创建数据库和用户...${NC}"
if [[ $DB_SERVICE == "mariadb" ]]; then
    sudo mariadb -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null || \
    mariadb -u root -p -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    
    sudo mariadb -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'${DB_HOST}' IDENTIFIED BY '${DB_PASSWORD}';" 2>/dev/null || \
    mariadb -u root -p -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'${DB_HOST}' IDENTIFIED BY '${DB_PASSWORD}';"
    
    sudo mariadb -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'${DB_HOST}';" 2>/dev/null || \
    mariadb -u root -p -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'${DB_HOST}';"
    
    sudo mariadb -e "FLUSH PRIVILEGES;" 2>/dev/null || \
    mariadb -u root -p -e "FLUSH PRIVILEGES;"
else
    sudo mysql -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null || \
    mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    
    sudo mysql -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'${DB_HOST}' IDENTIFIED BY '${DB_PASSWORD}';" 2>/dev/null || \
    mysql -u root -p -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'${DB_HOST}' IDENTIFIED BY '${DB_PASSWORD}';"
    
    sudo mysql -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'${DB_HOST}';" 2>/dev/null || \
    mysql -u root -p -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'${DB_HOST}';"
    
    sudo mysql -e "FLUSH PRIVILEGES;" 2>/dev/null || \
    mysql -u root -p -e "FLUSH PRIVILEGES;"
fi

echo -e "${GREEN}数据库配置完成${NC}"

# 4. 创建虚拟环境
echo -e "${GREEN}[4/8] 创建Python虚拟环境...${NC}"
python3 -m venv venv
source venv/bin/activate

# 5. 安装Python依赖
echo -e "${GREEN}[5/8] 安装Python依赖...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# 6. 配置环境变量
echo -e "${GREEN}[6/8] 配置环境变量...${NC}"
if [ ! -f .env ]; then
    cp env.example .env
    sed -i "s|DATABASE_URL=.*|DATABASE_URL=mysql+pymysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}|g" .env
    echo -e "${GREEN}.env文件已创建${NC}"
    echo -e "${GREEN}数据库连接字符串: mysql+pymysql://${DB_USER}:****@${DB_HOST}:${DB_PORT}/${DB_NAME}${NC}"
else
    echo -e "${YELLOW}.env文件已存在，跳过创建${NC}"
    echo -e "${YELLOW}如需修改配置，请手动编辑 .env 文件${NC}"
fi

# 7. 创建systemd服务
echo -e "${GREEN}[7/8] 创建systemd服务...${NC}"
CURRENT_USER=$(whoami)
CURRENT_DIR=$(pwd)

sudo tee /etc/systemd/system/bazi-api.service > /dev/null <<EOF
[Unit]
Description=Bazi API Service
After=network.target mysql.service

[Service]
Type=simple
User=${CURRENT_USER}
WorkingDirectory=${CURRENT_DIR}
Environment="PATH=${CURRENT_DIR}/venv/bin"
ExecStart=${CURRENT_DIR}/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 重载systemd
sudo systemctl daemon-reload

# 8. 启动服务
echo -e "${GREEN}[8/8] 启动服务...${NC}"
sudo systemctl start bazi-api
sudo systemctl enable bazi-api

# 检查服务状态
sleep 2
if sudo systemctl is-active --quiet bazi-api; then
    echo -e "${GREEN}✅ 服务启动成功！${NC}"
else
    echo -e "${RED}❌ 服务启动失败，请查看日志：${NC}"
    echo "sudo journalctl -u bazi-api -n 50"
    exit 1
fi

# 配置防火墙
echo -e "${GREEN}配置防火墙...${NC}"
if command -v ufw &> /dev/null; then
    sudo ufw allow 8000/tcp
    echo -e "${GREEN}已开放8000端口${NC}"
fi

# 显示部署信息
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}部署完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "API地址: ${YELLOW}http://$(hostname -I | awk '{print $1}'):8000${NC}"
echo -e "API文档: ${YELLOW}http://$(hostname -I | awk '{print $1}'):8000/docs${NC}"
echo ""
echo -e "${GREEN}常用命令：${NC}"
echo "  查看服务状态: sudo systemctl status bazi-api"
echo "  查看日志:     sudo journalctl -u bazi-api -f"
echo "  重启服务:     sudo systemctl restart bazi-api"
echo "  停止服务:     sudo systemctl stop bazi-api"
echo ""
echo -e "${YELLOW}注意：如需外网访问，请配置Nginx反向代理和SSL证书${NC}"
echo ""

