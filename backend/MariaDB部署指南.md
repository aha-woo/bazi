# MariaDB 部署指南

本项目完全支持 MariaDB 数据库（MariaDB 是 MySQL 的分支，完全兼容）。

## 🎯 使用现有 MariaDB 服务

### 方法一：使用自动部署脚本（推荐）

脚本会自动检测 MariaDB 服务：

```bash
cd backend
chmod +x deploy.sh
./deploy.sh
```

脚本会：
1. ✅ 自动检测 MariaDB/MySQL 服务
2. ✅ 询问是否使用现有数据库
3. ✅ 支持自定义数据库主机和端口
4. ✅ 自动创建数据库和用户
5. ✅ 配置正确的连接字符串

### 方法二：手动配置

#### 1. 准备 MariaDB 数据库

```bash
# 登录 MariaDB
sudo mariadb
# 或者
mariadb -u root -p
```

#### 2. 创建数据库和用户

```sql
-- 创建数据库
CREATE DATABASE bazi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户（本地连接）
CREATE USER 'bazi_user'@'localhost' IDENTIFIED BY 'your_strong_password';

-- 授予权限
GRANT ALL PRIVILEGES ON bazi_db.* TO 'bazi_user'@'localhost';

-- 刷新权限
FLUSH PRIVILEGES;

-- 退出
EXIT;
```

#### 3. 配置应用

```bash
cd backend

# 复制环境变量配置文件
cp env.example .env

# 编辑 .env 文件
nano .env
```

修改数据库连接字符串：

```env
# MariaDB 配置（使用 mysql+pymysql 驱动）
DATABASE_URL=mysql+pymysql://bazi_user:your_strong_password@localhost:3306/bazi_db

# API配置
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=False

# CORS配置
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

#### 4. 安装依赖并启动

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python -m uvicorn app.main:app --reload
```

## 🌐 远程 MariaDB 服务器

如果你的 MariaDB 在另一台服务器上：

### 1. 在 MariaDB 服务器上创建用户

```sql
-- 允许从特定 IP 访问
CREATE USER 'bazi_user'@'your_app_server_ip' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON bazi_db.* TO 'bazi_user'@'your_app_server_ip';

-- 或允许从任何主机访问（不推荐生产环境）
CREATE USER 'bazi_user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON bazi_db.* TO 'bazi_user'@'%';

FLUSH PRIVILEGES;
```

### 2. 修改 MariaDB 配置允许远程连接

```bash
# 编辑配置文件
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf

# 找到 bind-address 并修改为：
bind-address = 0.0.0.0

# 重启 MariaDB
sudo systemctl restart mariadb
```

### 3. 配置防火墙

```bash
# 开放 3306 端口
sudo ufw allow 3306/tcp
```

### 4. 应用配置

修改 `.env` 文件：

```env
DATABASE_URL=mysql+pymysql://bazi_user:password@mariadb_server_ip:3306/bazi_db
```

## 📊 MariaDB vs MySQL 区别

对于本项目来说，MariaDB 和 MySQL 完全兼容，使用方式完全相同：

| 特性 | MySQL | MariaDB | 支持情况 |
|------|-------|---------|---------|
| 驱动 | mysql+pymysql | mysql+pymysql | ✅ 相同 |
| 语法 | SQL | SQL | ✅ 兼容 |
| 端口 | 3306 | 3306 | ✅ 相同 |
| 连接方式 | TCP/Socket | TCP/Socket | ✅ 相同 |
| 字符集 | utf8mb4 | utf8mb4 | ✅ 支持 |

## 🔧 常见问题

### 1. 连接被拒绝

**错误**: `Can't connect to MariaDB server`

**解决方案**:
```bash
# 检查 MariaDB 是否运行
sudo systemctl status mariadb

# 启动 MariaDB
sudo systemctl start mariadb

# 检查端口监听
sudo netstat -tlnp | grep 3306
```

### 2. 认证失败

**错误**: `Access denied for user`

**解决方案**:
```sql
-- 重置用户密码
ALTER USER 'bazi_user'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

### 3. 数据库不存在

**错误**: `Unknown database 'bazi_db'`

**解决方案**:
```sql
-- 创建数据库
CREATE DATABASE bazi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 字符集问题

确保使用 utf8mb4：

```sql
-- 检查数据库字符集
SHOW CREATE DATABASE bazi_db;

-- 修改数据库字符集
ALTER DATABASE bazi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 🚀 使用自动部署脚本的示例

```bash
$ cd backend
$ ./deploy.sh

🚀 开始部署八字计算API...
[1/8] 更新系统...
[2/8] 安装系统依赖...
检测到的数据库服务：
  ✓ MariaDB (运行中)

是否使用现有的数据库服务? (y/n) [y]: y
将使用现有的 mariadb 服务
[3/8] 配置数据库...
请输入数据库名称 [bazi_db]: bazi_db
请输入数据库用户名 [bazi_user]: bazi_user
请输入数据库密码: ********
请输入数据库主机 [localhost]: localhost
请输入数据库端口 [3306]: 3306
创建数据库和用户...
数据库配置完成
[4/8] 创建Python虚拟环境...
[5/8] 安装Python依赖...
[6/8] 配置环境变量...
.env文件已创建
数据库连接字符串: mysql+pymysql://bazi_user:****@localhost:3306/bazi_db
[7/8] 创建systemd服务...
[8/8] 启动服务...
✅ 服务启动成功！

========================================
部署完成！
========================================

API地址: http://192.168.1.100:8000
API文档: http://192.168.1.100:8000/docs
```

## 💡 验证连接

部署完成后，可以通过以下方式验证：

### 1. 检查服务状态
```bash
sudo systemctl status bazi-api
```

### 2. 查看日志
```bash
sudo journalctl -u bazi-api -f
```

### 3. 测试 API
```bash
curl http://localhost:8000/health
```

### 4. 直接测试数据库连接
```bash
# 使用 Python 测试
python3 -c "
import pymysql
conn = pymysql.connect(
    host='localhost',
    user='bazi_user',
    password='your_password',
    database='bazi_db',
    charset='utf8mb4'
)
print('✅ 连接成功!')
conn.close()
"
```

## 📝 数据库备份

定期备份 MariaDB 数据：

```bash
# 备份数据库
mysqldump -u bazi_user -p bazi_db > bazi_backup_$(date +%Y%m%d).sql

# 恢复数据库
mysql -u bazi_user -p bazi_db < bazi_backup_20241025.sql
```

## 🔒 安全建议

1. **使用强密码**
   ```sql
   -- 密码应包含大小写字母、数字、特殊字符
   ALTER USER 'bazi_user'@'localhost' IDENTIFIED BY 'Str0ng!P@ssw0rd#2024';
   ```

2. **限制用户权限**
   ```sql
   -- 只授予必要的权限
   GRANT SELECT, INSERT, UPDATE, DELETE ON bazi_db.* TO 'bazi_user'@'localhost';
   ```

3. **使用 SSL 连接**（生产环境推荐）
   ```env
   DATABASE_URL=mysql+pymysql://user:pass@host:3306/db?ssl=true
   ```

4. **定期更新**
   ```bash
   sudo apt update
   sudo apt upgrade mariadb-server
   ```

## ✅ 总结

- ✅ MariaDB 完全兼容，无需修改代码
- ✅ 使用 `mysql+pymysql://` 连接字符串
- ✅ 自动部署脚本会检测并使用现有 MariaDB
- ✅ 支持本地和远程 MariaDB 服务器
- ✅ 完全支持 utf8mb4 字符集

如有问题，请查看日志或联系技术支持！

