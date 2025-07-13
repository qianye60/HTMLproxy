# HTML代理系统部署指南

## 部署配置检查结果

经过仔细检查，发现并修复了以下问题：

### ✅ 已修复的问题

1. **前端API请求配置**
   - 在 `front/src/main.ts` 中添加了 `axios.defaults.baseURL = '/api'`
   - 修复了 `front/src/pages/login.vue` 中的API请求路径

2. **Nginx代理配置**
   - 修复了 `nginx.conf` 中的Docker服务名引用
   - 将 `127.0.0.1:40000` 改为 `backend:40000`

3. **Docker网络配置**
   - 在 `docker-compose.yml` 中添加了自定义网络
   - 确保nginx和backend服务在同一网络中

4. **启动脚本优化**
   - 在 `start.sh` 中添加了等待后端启动的逻辑

5. **端口配置优化**
   - 将外部端口从80改为8080，避免与系统服务冲突
   - 更适合域名代理部署

### 🔧 部署步骤

1. **构建并启动服务**
   ```bash
   docker-compose up --build
   ```

2. **验证部署**
   ```bash
   # 检查容器状态
   docker-compose ps
   
   # 查看日志
   docker-compose logs nginx
   docker-compose logs backend
   ```

3. **测试访问**
   - 前端: http://localhost:8080
   - 后端API: http://localhost:8080/api/
   - HTML文件: http://localhost:8080/html/{username}/{filename}

### 🌐 域名代理配置

#### 使用Nginx反向代理（推荐）

1. **安装Nginx**
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. **创建Nginx配置文件**
   ```bash
   sudo nano /etc/nginx/sites-available/htmlproxy
   ```

3. **配置内容**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;  # 替换为你的域名
       
       location / {
           proxy_pass http://localhost:8080;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

4. **启用配置**
   ```bash
   sudo ln -s /etc/nginx/sites-available/htmlproxy /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

#### 使用Caddy（更简单）

1. **安装Caddy**
   ```bash
   sudo apt install caddy
   ```

2. **创建Caddyfile**
   ```bash
   sudo nano /etc/caddy/Caddyfile
   ```

3. **配置内容**
   ```
   your-domain.com {
       reverse_proxy localhost:8080
   }
   ```

4. **重启Caddy**
   ```bash
   sudo systemctl restart caddy
   ```

### 📋 配置说明

#### Nginx配置 (`nginx.conf`)
```nginx
# 前端静态资源
location / {
    root   /usr/share/nginx/html;
    try_files $uri $uri/ /index.html;
    index  index.html;
}

# 后端API代理
location /api/ {
    proxy_pass http://backend:40000/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# HTML文件访问
location /html/ {
    proxy_pass http://backend:40000/html/;
}
```

#### 前端API配置
- 所有API请求都会自动添加 `/api` 前缀
- 登录/注册请求路径: `/login`, `/register`
- 其他API请求路径: `/user/info`, `/files`, `/upload` 等

#### 后端路由配置
- 所有API路由都带有 `/api` 前缀
- HTML文件访问路由: `/api/html/{username}/{filename}`

### 🚨 注意事项

1. **端口配置**
   - 前端访问端口: 8080 (开发环境)
   - 生产环境通过域名访问 (80/443)
   - 后端服务端口: 40000 (内部)
   - 确保8080端口未被占用

2. **文件权限**
   - 确保 `data/`, `html_files/`, `uploads/` 目录有正确的读写权限

3. **网络配置**
   - 使用Docker网络确保容器间通信正常
   - 前端通过nginx代理访问后端API

4. **域名配置**
   - 确保域名DNS解析正确
   - 配置SSL证书（推荐使用Let's Encrypt）
   - 设置防火墙规则

### 🔍 故障排除

1. **前端无法访问后端API**
   - 检查nginx配置中的代理路径
   - 确认backend服务正常运行
   - 查看nginx错误日志

2. **HTML文件无法访问**
   - 检查文件路径是否正确
   - 确认后端文件服务路由正常
   - 验证文件权限

3. **登录功能异常**
   - 检查API请求路径是否正确
   - 确认JWT token配置
   - 查看后端认证日志

4. **域名访问问题**
   - 检查DNS解析是否正确
   - 确认防火墙设置
   - 验证SSL证书配置

### 📝 部署验证清单

- [ ] Docker容器正常启动
- [ ] 本地访问正常 (http://localhost:8080)
- [ ] 域名解析正确
- [ ] 域名访问正常
- [ ] SSL证书配置正确
- [ ] 用户注册功能正常
- [ ] 用户登录功能正常
- [ ] 文件上传功能正常
- [ ] HTML文件可以访问
- [ ] 文件管理功能正常

### 🔒 SSL证书配置

#### 使用Let's Encrypt (推荐)

1. **安装Certbot**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **获取SSL证书**
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

3. **自动续期**
   ```bash
   sudo crontab -e
   # 添加以下行
   0 12 * * * /usr/bin/certbot renew --quiet
   ```

部署配置已经修复完成，现在支持域名代理部署！ 