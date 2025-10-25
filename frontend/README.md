# 八字计算器前端测试页面

这是一个简单的测试页面，用于测试八字计算API。

## 功能特点

- ✅ 美观的现代化UI设计
- ✅ 实时调用API
- ✅ 支持自定义API地址
- ✅ 四柱可视化显示
- ✅ 五行分析图表
- ✅ 完整的命理解读
- ✅ 响应式设计（支持手机访问）
- ✅ 错误处理和提示

## 使用方法

### 方法一：直接打开（推荐）

1. 确保后端API服务已启动（默认地址：http://localhost:8000）
2. 直接双击 `index.html` 文件，用浏览器打开
3. 输入出生信息，点击"开始计算"按钮

### 方法二：使用本地服务器

如果遇到CORS跨域问题，可以使用本地服务器：

#### Python方式
```bash
# Python 3
cd frontend
python -m http.server 8080

# Python 2
python -m SimpleHTTPServer 8080
```

然后访问：http://localhost:8080

#### Node.js方式
```bash
# 安装http-server
npm install -g http-server

# 启动服务
cd frontend
http-server -p 8080
```

然后访问：http://localhost:8080

#### VS Code Live Server
如果使用VS Code，安装"Live Server"插件，右键点击`index.html`，选择"Open with Live Server"。

## 配置API地址

如果你的API服务不在 `http://localhost:8000`，可以在页面上修改"API服务地址"输入框。

例如：
- 本地：`http://localhost:8000`
- 局域网：`http://192.168.1.100:8000`
- 远程服务器：`http://your-domain.com` 或 `https://api.your-domain.com`

## 快捷键

- **Ctrl + T**: 快速填充测试数据

## 测试数据

默认测试数据：
- 出生日期：1990年5月15日
- 出生时间：14:30
- 时区：Asia/Shanghai（北京时间）

## 常见问题

### 1. 无法连接到API

**问题**：点击"开始计算"后显示连接错误

**解决方案**：
- 确保后端服务已启动（运行 `cd backend && python -m uvicorn app.main:app --reload`）
- 检查API地址是否正确
- 检查防火墙设置
- 如果后端在另一台机器上，确保网络可达

### 2. CORS跨域错误

**问题**：浏览器控制台显示CORS错误

**解决方案**：
- 后端已经配置了CORS，允许所有域名访问
- 如果仍有问题，使用本地服务器运行前端（见上面"方法二"）

### 3. 计算结果不准确

**问题**：八字计算结果与其他工具不同

**说明**：
- 不同的八字计算工具可能使用不同的算法
- 时区设置非常重要，确保选择正确的出生时区
- 月柱计算涉及节气，目前使用简化算法（以2月4日立春为界）

## 部署到生产环境

### 直接部署静态文件

将 `frontend` 文件夹中的所有文件上传到你的Web服务器（如Nginx、Apache）。

#### Nginx配置示例

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    root /var/www/bazi-frontend;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### 使用CDN

可以将静态文件部署到：
- GitHub Pages
- Netlify
- Vercel
- Cloudflare Pages

## API集成示例

如果你想将八字计算功能集成到自己的项目中，可以参考以下代码：

### JavaScript调用示例

```javascript
async function calculateBazi(birthData) {
    const response = await fetch('http://your-api-url/api/v1/bazi/calculate', {
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
    return data;
}
```

### jQuery调用示例

```javascript
$.ajax({
    url: 'http://your-api-url/api/v1/bazi/calculate',
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({
        year: 1990,
        month: 5,
        day: 15,
        hour: 14,
        minute: 30,
        timezone: 'Asia/Shanghai'
    }),
    success: function(data) {
        console.log(data);
    }
});
```

## 移动端适配

页面已做响应式设计，可以在手机、平板上正常使用。

在移动设备上访问时，布局会自动调整为单列显示。

## 浏览器兼容性

支持所有现代浏览器：
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

## 下一步

如果你想要更专业的前端应用，可以考虑：

1. **React/Vue/Angular**: 使用现代前端框架重构
2. **移动App**: 使用React Native或Flutter开发
3. **小程序**: 开发微信小程序版本
4. **PWA**: 将Web应用转换为Progressive Web App

## 技术栈

- **纯HTML5**: 语义化标签
- **CSS3**: Grid布局、渐变、动画
- **原生JavaScript**: ES6+语法，Fetch API
- **无依赖**: 不需要任何第三方库

## 许可证

MIT License

---

**祝您使用愉快！** 🎉

