# 八字计算API服务

专业的八字命理计算服务，支持跨平台调用（Web、iOS、Android）

## 🌟 功能特点

- ✅ 精准的八字四柱计算（年、月、日、时）
- ✅ 五行分析和平衡评估
- ✅ 命理解读和性格分析
- ✅ 喜用神推算
- ✅ 运势建议（颜色、方位、职业）
- ✅ 支持多时区
- ✅ MySQL数据库存储
- ✅ RESTful API设计
- ✅ 完整的API文档（Swagger）
- ✅ 跨域支持（CORS）

## 📋 技术栈

- **后端框架**: FastAPI 0.104+
- **数据库**: MySQL 5.7+
- **ORM**: SQLAlchemy 2.0+
- **Python**: 3.8+
- **服务器**: Uvicorn

## 🚀 快速开始

### 1. 环境准备

确保你的系统已安装：
- Python 3.8+
- MySQL 5.7+
- pip

### 2. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置数据库

#### 创建MySQL数据库

```sql
CREATE DATABASE bazi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 配置环境变量

复制 `env.example` 为 `.env` 并修改配置：

```bash
cp env.example .env
```

编辑 `.env` 文件：

```env
# 数据库配置（修改为你的实际配置）
DATABASE_URL=mysql+pymysql://your_username:your_password@localhost:3306/bazi_db

# API配置
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=False

# CORS配置
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080", "https://yourdomain.com"]
```

### 4. 运行服务

#### 开发模式（带自动重载）

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 生产模式

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 访问API文档

服务启动后，访问以下地址：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API根路径**: http://localhost:8000/

## 📡 API接口说明

### 1. 计算八字

**POST** `/api/v1/bazi/calculate`

计算用户的八字四柱和命理解读。

**请求示例：**

```bash
curl -X POST "http://localhost:8000/api/v1/bazi/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "year": 1990,
    "month": 5,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "timezone": "Asia/Shanghai",
    "user_id": "user123"
  }'
```

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| year | int | 是 | 出生年份 (1900-2100) |
| month | int | 是 | 出生月份 (1-12) |
| day | int | 是 | 出生日期 (1-31) |
| hour | int | 是 | 出生小时 (0-23) |
| minute | int | 否 | 出生分钟 (0-59)，默认0 |
| timezone | string | 否 | 时区，默认 Asia/Shanghai |
| user_id | string | 否 | 用户ID |

**响应示例：**

```json
{
  "id": 1,
  "birth_time": "1990-05-15T14:30:00+08:00",
  "timezone": "Asia/Shanghai",
  "year_pillar": "庚午",
  "month_pillar": "辛巳",
  "day_pillar": "甲子",
  "hour_pillar": "辛未",
  "rigan": "甲",
  "rigan_wuxing": "木",
  "wuxing_analysis": {
    "count": {
      "木": 1,
      "火": 2,
      "土": 1,
      "金": 2,
      "水": 2
    },
    "strongest": "火",
    "weakest": "木",
    "total": 8
  },
  "interpretation": {
    "basic": "您的日主为甲，五行属木。",
    "wuxing_distribution": "您的八字中，木有1个，火有2个，土有1个，金有2个，水有2个。",
    "wuxing_balance": "五行中火最旺，木最弱。",
    "personality": "甲木日主，如参天大树...",
    "xiyongshen": "建议以木为喜用神...",
    "advice": "颜色方面：可多穿戴绿色、青色系的衣物...",
    "full_text": "完整解读文本..."
  },
  "sizhu": {
    "year": {"ganzhi": "庚午", "tian": "庚", "di": "午"},
    "month": {"ganzhi": "辛巳", "tian": "辛", "di": "巳"},
    "day": {"ganzhi": "甲子", "tian": "甲", "di": "子"},
    "hour": {"ganzhi": "辛未", "tian": "辛", "di": "未"}
  }
}
```

### 2. 查询八字记录

**GET** `/api/v1/bazi/record/{record_id}`

根据记录ID查询八字信息。

**请求示例：**

```bash
curl -X GET "http://localhost:8000/api/v1/bazi/record/1"
```

### 3. 查询用户记录列表

**GET** `/api/v1/bazi/user/{user_id}`

查询某个用户的所有八字记录。

**请求示例：**

```bash
curl -X GET "http://localhost:8000/api/v1/bazi/user/user123?skip=0&limit=10"
```

### 4. 获取时区列表

**GET** `/api/v1/timezones`

获取支持的时区列表。

**请求示例：**

```bash
curl -X GET "http://localhost:8000/api/v1/timezones"
```

### 5. 健康检查

**GET** `/health`

检查服务运行状态。

**请求示例：**

```bash
curl -X GET "http://localhost:8000/health"
```

## 🌍 时区支持

API支持全球时区，常用时区包括：

- `Asia/Shanghai` - 北京时间 (UTC+8)
- `Asia/Hong_Kong` - 香港 (UTC+8)
- `Asia/Taipei` - 台北 (UTC+8)
- `Asia/Tokyo` - 东京 (UTC+9)
- `America/New_York` - 纽约 (UTC-5/-4)
- `Europe/London` - 伦敦 (UTC+0/+1)

完整时区列表可通过 `/api/v1/timezones` 接口获取。

## 📦 部署到Ubuntu VPS

### 方法一：使用系统服务（推荐）

#### 1. 上传代码到服务器

```bash
# 在本地打包
tar -czf bazi-api.tar.gz backend/

# 上传到服务器
scp bazi-api.tar.gz user@your-server-ip:/home/user/

# SSH登录服务器
ssh user@your-server-ip

# 解压
tar -xzf bazi-api.tar.gz
cd backend
```

#### 2. 安装依赖

```bash
# 安装Python和pip
sudo apt update
sudo apt install python3 python3-pip python3-venv mysql-server -y

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 3. 配置数据库

```bash
# 登录MySQL
sudo mysql

# 创建数据库和用户
CREATE DATABASE bazi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bazi_user'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON bazi_db.* TO 'bazi_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 4. 配置环境变量

```bash
# 创建.env文件
nano .env
```

填入配置：

```env
DATABASE_URL=mysql+pymysql://bazi_user:your_strong_password@localhost:3306/bazi_db
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=False
CORS_ORIGINS=["https://yourdomain.com"]
```

#### 5. 创建systemd服务

```bash
sudo nano /etc/systemd/system/bazi-api.service
```

填入内容：

```ini
[Unit]
Description=Bazi API Service
After=network.target mysql.service

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/backend
Environment="PATH=/home/your_username/backend/venv/bin"
ExecStart=/home/your_username/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 6. 启动服务

```bash
# 重载systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start bazi-api

# 设置开机自启
sudo systemctl enable bazi-api

# 查看状态
sudo systemctl status bazi-api
```

#### 7. 配置Nginx反向代理（可选）

```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/bazi-api
```

填入配置：

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用站点：

```bash
sudo ln -s /etc/nginx/sites-available/bazi-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 8. 配置防火墙

```bash
sudo ufw allow 8000/tcp  # API端口
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 方法二：使用Docker（简化部署）

#### 1. 创建Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### 2. 创建docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://bazi_user:password@db:3306/bazi_db
    depends_on:
      - db
    restart: always

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=bazi_db
      - MYSQL_USER=bazi_user
      - MYSQL_PASSWORD=password
    volumes:
      - mysql_data:/var/lib/mysql
    restart: always

volumes:
  mysql_data:
```

#### 3. 部署

```bash
docker-compose up -d
```

## 🔧 客户端调用示例

### JavaScript (Web)

```javascript
async function calculateBazi(birthData) {
  const response = await fetch('http://your-server-ip:8000/api/v1/bazi/calculate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      year: 1990,
      month: 5,
      day: 15,
      hour: 14,
      minute: 30,
      timezone: 'Asia/Shanghai',
      user_id: 'user123'
    })
  });
  
  const data = await response.json();
  console.log(data);
  return data;
}
```

### iOS (Swift)

```swift
struct BaziRequest: Codable {
    let year: Int
    let month: Int
    let day: Int
    let hour: Int
    let minute: Int
    let timezone: String
    let userId: String?
}

func calculateBazi(request: BaziRequest, completion: @escaping (Result<BaziResponse, Error>) -> Void) {
    let url = URL(string: "http://your-server-ip:8000/api/v1/bazi/calculate")!
    var urlRequest = URLRequest(url: url)
    urlRequest.httpMethod = "POST"
    urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
    
    let encoder = JSONEncoder()
    urlRequest.httpBody = try? encoder.encode(request)
    
    URLSession.shared.dataTask(with: urlRequest) { data, response, error in
        // Handle response
    }.resume()
}
```

### Android (Kotlin)

```kotlin
data class BaziRequest(
    val year: Int,
    val month: Int,
    val day: Int,
    val hour: Int,
    val minute: Int,
    val timezone: String,
    val userId: String?
)

fun calculateBazi(request: BaziRequest) {
    val client = OkHttpClient()
    val json = Gson().toJson(request)
    val body = json.toRequestBody("application/json".toMediaType())
    
    val httpRequest = Request.Builder()
        .url("http://your-server-ip:8000/api/v1/bazi/calculate")
        .post(body)
        .build()
    
    client.newCall(httpRequest).enqueue(object : Callback {
        override fun onResponse(call: Call, response: Response) {
            // Handle response
        }
        override fun onFailure(call: Call, e: IOException) {
            // Handle error
        }
    })
}
```

## 🛡️ 安全建议

1. **生产环境配置**
   - 修改数据库密码为强密码
   - 配置具体的CORS域名（不要使用*）
   - 启用HTTPS（使用Let's Encrypt）
   - 限制API访问频率（使用slowapi等）

2. **数据库安全**
   - 定期备份数据库
   - 限制MySQL远程访问
   - 使用独立的数据库用户

3. **服务器安全**
   - 配置防火墙
   - 定期更新系统和依赖
   - 使用非root用户运行服务

## 📊 性能优化

1. **数据库优化**
   - 为常用字段添加索引
   - 使用连接池
   - 定期清理旧数据

2. **API优化**
   - 使用多worker运行（uvicorn --workers 4）
   - 添加Redis缓存（可选）
   - 配置Nginx负载均衡

3. **监控**
   - 使用Prometheus + Grafana监控
   - 配置日志记录
   - 设置告警

## 📝 开发说明

### 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI主应用
│   ├── models.py            # 数据库模型
│   ├── schemas.py           # Pydantic数据模型
│   ├── database.py          # 数据库配置
│   ├── bazi_calculator.py   # 八字计算核心算法
│   └── crud.py              # 数据库CRUD操作
├── requirements.txt         # Python依赖
├── env.example             # 环境变量示例
└── README.md               # 本文档
```

### 添加新功能

1. 在 `bazi_calculator.py` 中添加算法
2. 在 `schemas.py` 中定义数据模型
3. 在 `main.py` 中添加API端点
4. 更新文档

## ❓ 常见问题

### 1. 数据库连接失败

检查：
- MySQL服务是否运行
- 数据库配置是否正确
- 用户权限是否足够

### 2. 端口被占用

```bash
# 查看端口占用
lsof -i :8000

# 修改端口
export API_PORT=8001
```

### 3. 跨域问题

在 `.env` 中配置 `CORS_ORIGINS`：

```env
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

## 📞 支持

如有问题，请联系开发者或提交Issue。

## 📄 许可证

MIT License

---

**祝您使用愉快！** 🎉

