# DHJ的小站

一个基于 Flask 框架开发的个人博客网站，支持图片分享、评论互动等功能。

## 功能特性

- 📷 **图片分享** - 支持批量上传图片，附带文字说明
- 💬 **评论系统** - 用户可以对图片进行评论和回复
- 🔐 **用户认证** - 注册、登录、密码重置（邮箱验证码）
- 👤 **个人中心** - 用户资料管理、头像上传
- 📊 **管理面板** - 管理员可以管理用户和内容
- 🔔 **消息通知** - 评论回复通知功能

## 技术栈

- **框架**: Flask 3.x
- **数据库**: SQLite
- **前端**: HTML5 + CSS3 + JavaScript
- **认证**: Flask-Login + Flask-Bcrypt
- **安全**: Flask-WTF（全站 CSRF 防护）
- **邮件**: Flask-Mail（配置在 `.env`，不配置时验证码打印到控制台，仅限开发）

## 快速开始

### 环境要求

- Python 3.10+
- pip 包管理器

### 安装步骤

```bash
# 克隆项目
git clone https://github.com/DHJ999/mini_personal_blog.git
cd mini_personal_blog

# 创建并激活虚拟环境（Windows 用 venv\Scripts\activate）
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量模板并填写（SECRET_KEY / 邮件配置 / 管理员账号）
# Windows: copy .env.example .env
cp .env.example .env

# 初始化数据库并运行（开发模式）
FLASK_DEBUG=1 python app.py
```

### 访问网站

打开浏览器访问: http://localhost:5000

## 项目结构

```
mini_personal_blog/
├── app.py              # 主应用文件
├── .env.example        # 环境变量模板（复制为 .env 使用，勿提交 .env）
├── .gitignore
├── requirements.txt    # 依赖清单
├── static/             # 静态文件目录
│   ├── style.css       # 样式文件
│   └── uploads/        # 上传的图片目录（运行期产生，不入库）
├── instance/
│   └── blog.db         # SQLite 数据库（运行期产生，不入库）
└── templates/          # 模板文件目录
    ├── index.html      # 首页
    ├── login.html      # 登录页
    ├── register.html   # 注册页
    ├── profile.html    # 个人中心
    └── admin.html      # 管理面板
```

## 配置说明（.env）

所有敏感配置通过 `.env` / 环境变量注入，**不要**硬编码进代码或提交到仓库：

| 变量 | 说明 |
| --- | --- |
| `SECRET_KEY` | 会话密钥，用 `python -c "import secrets;print(secrets.token_hex(32))"` 生成 |
| `MAIL_USERNAME` / `MAIL_PASSWORD` | SMTP 邮箱及授权码；留空时验证码打印到控制台（仅开发） |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | 首次启动自动创建的管理员；不设置时仅开发模式创建 `admin/admin123` |
| `FLASK_DEBUG` | `1` = 调试模式（勿用于生产） |
| `HOST` / `PORT` | 监听地址与端口，默认 `127.0.0.1:5000` |

## 部署说明（生产环境）

```bash
pip install waitress
# 建议关闭调试并配置好 SECRET_KEY、ADMIN_*、MAIL_* 环境变量
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

生产环境务必注意：
- `FLASK_DEBUG=0`，用 waitress/gunicorn 等正式 WSGI 服务器；
- 通过环境变量设置随机的 `SECRET_KEY` 与管理员密码；
- 不要在前置 Nginx/反代下直接暴露 debug 服务。

## 安全说明

- 全站已启用 CSRF 防护（Flask-WTF），所有 POST 操作需携带 `csrf_token`；
- 删除/标记已读等有副作用的操作仅接受 POST；
- 数据库、上传文件、`.env` 均已被 `.gitignore` 排除，不会进入版本库。

---

Made with ❤️ For you for me
