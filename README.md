# 🔮 八字命理计算系统

一个专业的八字命理计算API服务，支持跨平台调用（Web、iOS、Android）。

## 📁 项目结构

```
bazi/
├── backend/              # 后端API服务
│   ├── app/             # 应用代码
│   │   ├── main.py      # FastAPI主应用
│   │   ├── bazi_calculator.py  # 八字计算核心算法
│   │   ├── models.py    # 数据库模型
│   │   ├── schemas.py   # API数据模型
│   │   ├── database.py  # 数据库配置
│   │   └── crud.py      # 数据库操作
│   ├── requirements.txt # Python依赖
│   ├── env.example     # 环境变量示例
│   ├── deploy.sh       # Ubuntu部署脚本
│   ├── start_dev.sh    # Linux/Mac开发启动脚本
│   ├── start_dev.bat   # Windows开发启动脚本
│   └── README.md       # 后端详细文档
├── frontend/            # 前端测试页面
│   ├── index.html      # 主页面
│   ├── app.js          # JavaScript逻辑
│   └── README.md       # 前端使用说明
└── README.md           # 本文档
```

## ✨ 功能特点

### 后端API
- ✅ 精准的八字四柱计算（年月日时）
- ✅ 天干地支自动推算
- ✅ 五行分析和平衡评估
- ✅ 命理解读和性格分析
- ✅ 喜用神推算
- ✅ 运势建议（颜色、方位、职业）
- ✅ 支持全球时区
- ✅ MySQL数据库持久化存储
- ✅ RESTful API设计
- ✅ 完整的Swagger API文档
- ✅ CORS跨域支持

### 前端界面
- ✅ 现代化美观UI设计
- ✅ 响应式布局（支持手机、平板）
- ✅ 实时API调用
- ✅ 四柱可视化展示
- ✅ 五行分析图表
- ✅ 完整的命理解读显示

## 🚀 快速开始

### 第一步：启动后端API服务

#### Windows系统

1. **安装Python和MySQL**
   - 下载安装 Python 3.8+ (https://www.python.org/)
   - 下载安装 MySQL 5.7+ (https://dev.mysql.com/downloads/mysql/)

2. **配置数据库**
   ```sql
   -- 登录MySQL，创建数据库
   CREATE DATABASE bazi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **启动开发服务器**
   ```cmd
   cd backend
   start_dev.bat
   ```
   
   第一次运行会自动创建虚拟环境并安装依赖。

4. **手动配置（可选）**
   如果需要修改数据库配置：
   ```cmd
   cd backend
   copy env.example .env
   notepad .env
   ```
   
   修改数据库连接信息：
   ```
   DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/bazi_db
   ```

#### Linux/Mac系统

1. **安装依赖**
   ```bash
   # Ubuntu/Debian
   sudo apt install python3 python3-pip python3-venv mysql-server
   
   # macOS (使用Homebrew)
   brew install python mysql
   ```

2. **配置数据库**
   ```bash
   # 登录MySQL
   mysql -u root -p
   
   # 创建数据库
   CREATE DATABASE bazi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   EXIT;
   ```

3. **启动开发服务器**
   ```bash
   cd backend
   chmod +x start_dev.sh
   ./start_dev.sh
   ```

4. **手动配置（可选）**
   ```bash
   cd backend
   cp env.example .env
   nano .env  # 或使用 vim、code 等编辑器
   ```

### 第二步：打开前端测试页面

1. **确保后端服务已启动**（看到"Application startup complete"提示）

2. **打开前端页面**
   - 直接双击 `frontend/index.html` 文件
   - 或使用浏览器打开该文件

3. **输入出生信息并测试**
   - 默认已填充测试数据（1990年5月15日 14:30）
   - 点击"🔮 开始计算"按钮
   - 查看八字解读结果

### 第三步：验证API功能

访问以下地址查看API文档和测试：

- **API根路径**: http://localhost:8000
- **Swagger文档**: http://localhost:8000/docs （可在线测试所有API）
- **ReDoc文档**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

## 📡 API接口说明

### 主要接口

#### 1. 计算八字
```
POST /api/v1/bazi/calculate
```

**请求体示例：**
```json
{
  "year": 1990,
  "month": 5,
  "day": 15,
  "hour": 14,
  "minute": 30,
  "timezone": "Asia/Shanghai",
  "user_id": "user123"
}
```

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
    "count": {"木": 1, "火": 2, "土": 1, "金": 2, "水": 2},
    "strongest": "火",
    "weakest": "木"
  },
  "interpretation": {
    "basic": "您的日主为甲，五行属木。",
    "personality": "甲木日主，如参天大树...",
    "xiyongshen": "建议以木为喜用神...",
    "advice": "颜色方面：可多穿戴绿色、青色系的衣物..."
  }
}
```

#### 2. 查询记录
```
GET /api/v1/bazi/record/{record_id}    # 查询单条记录
GET /api/v1/bazi/user/{user_id}        # 查询用户记录
GET /api/v1/bazi/records               # 查询所有记录
```

#### 3. 其他接口
```
GET /api/v1/timezones                  # 获取时区列表
GET /health                            # 健康检查
DELETE /api/v1/bazi/record/{id}        # 删除记录
```

完整API文档请访问：http://localhost:8000/docs

## 🌍 部署到生产环境（Ubuntu VPS）

### 自动部署（推荐）

```bash
# 1. 上传代码到服务器
scp -r backend user@your-server-ip:/home/user/bazi-api

# 2. SSH登录服务器
ssh user@your-server-ip

# 3. 运行部署脚本
cd /home/user/bazi-api/backend
chmod +x deploy.sh
./deploy.sh
```

脚本会自动完成：
- 安装系统依赖（Python、MySQL、Nginx）
- 配置数据库
- 创建虚拟环境
- 安装Python依赖
- 配置systemd服务
- 启动API服务

### 手动部署

详细的手动部署步骤请查看：`backend/README.md`

包括：
- systemd服务配置
- Nginx反向代理配置
- SSL证书配置（HTTPS）
- 防火墙配置
- Docker部署方式

### 服务管理命令

```bash
# 查看服务状态
sudo systemctl status bazi-api

# 启动服务
sudo systemctl start bazi-api

# 停止服务
sudo systemctl stop bazi-api

# 重启服务
sudo systemctl restart bazi-api

# 查看日志
sudo journalctl -u bazi-api -f

# 设置开机自启
sudo systemctl enable bazi-api
```

## 🔧 客户端调用示例

### JavaScript (Web)
```javascript
async function calculateBazi() {
  const response = await fetch('http://your-server:8000/api/v1/bazi/calculate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      year: 1990,
      month: 5,
      day: 15,
      hour: 14,
      minute: 30,
      timezone: 'Asia/Shanghai'
    })
  });
  const data = await response.json();
  console.log(data);
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
}

let url = URL(string: "http://your-server:8000/api/v1/bazi/calculate")!
var request = URLRequest(url: url)
request.httpMethod = "POST"
request.setValue("application/json", forHTTPHeaderField: "Content-Type")
request.httpBody = try? JSONEncoder().encode(baziRequest)

URLSession.shared.dataTask(with: request) { data, response, error in
    // Handle response
}.resume()
```

### Android (Kotlin + Retrofit)
```kotlin
interface BaziApi {
    @POST("api/v1/bazi/calculate")
    suspend fun calculateBazi(@Body request: BaziRequest): BaziResponse
}

data class BaziRequest(
    val year: Int,
    val month: Int,
    val day: Int,
    val hour: Int,
    val minute: Int,
    val timezone: String
)
```

## 📊 技术栈

### 后端
- **语言**: Python 3.8+
- **框架**: FastAPI 0.104+
- **数据库**: MySQL 5.7+
- **ORM**: SQLAlchemy 2.0+
- **服务器**: Uvicorn
- **部署**: systemd + Nginx

### 前端
- **HTML5**: 语义化标签
- **CSS3**: Grid布局、渐变、动画
- **JavaScript**: ES6+、Fetch API
- **无依赖**: 纯原生实现

## 🎯 使用场景

1. **命理网站/APP**
   - 在线八字排盘服务
   - 命理咨询平台
   - 风水命理APP

2. **小程序/H5应用**
   - 微信小程序
   - 支付宝小程序
   - H5移动页面

3. **企业内部系统**
   - HR系统集成
   - CRM系统功能扩展

4. **教育学习**
   - 命理教学工具
   - 学生作业系统

## 📖 详细文档

- **后端API文档**: `backend/README.md`
- **前端使用说明**: `frontend/README.md`
- **在线API文档**: http://localhost:8000/docs

## 🔐 安全建议

### 开发环境
- ✅ 已配置，可直接使用

### 生产环境
- ⚠️ 修改MySQL密码为强密码
- ⚠️ 配置具体的CORS域名（不要使用*）
- ⚠️ 启用HTTPS（使用Let's Encrypt）
- ⚠️ 配置API访问频率限制
- ⚠️ 配置防火墙规则
- ⚠️ 定期备份数据库
- ⚠️ 使用非root用户运行服务

## ❓ 常见问题

### 1. 后端启动失败

**原因**：通常是数据库连接问题

**解决**：
```bash
# 检查MySQL是否运行
sudo systemctl status mysql  # Linux
# 或在Windows服务中检查MySQL服务

# 检查数据库配置
cat backend/.env  # 查看DATABASE_URL是否正确
```

### 2. 前端无法连接API

**原因**：CORS或网络问题

**解决**：
- 确保后端服务已启动
- 检查API地址是否正确
- 查看浏览器控制台错误信息
- 使用本地服务器运行前端（见frontend/README.md）

### 3. 八字计算结果与其他工具不同

**说明**：
- 不同工具算法可能有差异
- 时区设置非常重要
- 月柱计算涉及节气，当前使用简化算法

### 4. 数据库连接报错

**错误信息**：`Can't connect to MySQL server`

**解决**：
```bash
# 检查MySQL服务
sudo systemctl start mysql

# 测试连接
mysql -u root -p

# 检查用户权限
SHOW GRANTS FOR 'bazi_user'@'localhost';
```

## 📈 性能优化

- **数据库**: 添加索引、使用连接池
- **API**: 使用多worker、添加缓存
- **部署**: 使用Nginx负载均衡、CDN加速

详见：`backend/README.md` 性能优化章节

## 🔄 更新日志

### Version 1.0.0 (2024)
- ✨ 初始版本发布
- ✅ 完整的八字计算功能
- ✅ RESTful API
- ✅ MySQL数据库支持
- ✅ 前端测试页面
- ✅ 部署脚本和文档

## 📝 待开发功能

- [ ] 大运推算
- [ ] 流年分析
- [ ] 合婚配对
- [ ] 择日功能
- [ ] 用户认证系统
- [ ] Redis缓存
- [ ] 更精确的节气计算
- [ ] 多语言支持（英文、繁体等）

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📞 技术支持

如有问题，请查看详细文档或提交Issue。

---

**祝您使用愉快！** 🎉

## 快速测试清单

- [ ] 后端服务启动成功（访问 http://localhost:8000）
- [ ] 数据库连接正常（检查日志无错误）
- [ ] API文档可访问（http://localhost:8000/docs）
- [ ] 前端页面打开正常
- [ ] 提交测试数据返回正确结果
- [ ] 四柱显示正确（年月日时）
- [ ] 五行分析正确
- [ ] 命理解读显示正常

全部通过？恭喜！系统运行正常 ✅

