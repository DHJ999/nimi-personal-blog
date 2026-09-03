<div align="center">

# 🏠 DHJ 的小站

**一个基于 Flask 的轻量个人博客** —— 图片分享、评论互动、消息通知，开箱即用。

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Frontend](https://img.shields.io/badge/Frontend-HTML%20%2F%20CSS%20%2F%20JS-E34F26?logo=html5&logoColor=white)]()
[![CSRF](https://img.shields.io/badge/CSRF-Protected-success)]()
[![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-ff69b4)]()

📘 **English version**: [README_EN.md](README_EN.md)

</div>

---

## 📖 项目简介

个人图片博客系统，主打**轻量与私密**：注册用户可上传、分享图片，访客与用户之间可评论、回复互动，回复会以站内消息形式实时通知对方；管理员拥有独立的统计后台与内容管理面板。

技术上一个 `app.py` 即可跑通全部功能，适合个人学习 Flask 全栈、或作为小型家庭/好友共享相册使用。

## ✨ 功能特性

| 分类 | 功能 |
| --- | --- |
| 📷 图片分享 | 单张 / 批量上传，按批次聚合展示（`uploads/` 本地存储） |
| 💬 评论互动 | 图片详情页评论、批次评论区，支持**多级回复** |
| 🔔 消息通知 | 评论 / 回复自动生成站内消息，未读角标提醒、一键全部已读 |
| 🔐 账号体系 | 邮箱验证码注册、登录、**忘记密码（邮件重置）**、密码加密存储（bcrypt） |
| 👤 个人中心 | 修改昵称 / 邮箱 / 密码，自定义头像上传 |
| 🛡️ 权限控制 | 访客可浏览；发评论、后台管理需登录；管理员专属面板 |
| 📊 数据统计 | 访问量、图片数、评论数、消息数等运营数据看板（`/admin/analytics`） |
| ⚙️ 消息管理 | 评论 / 回复通知列表、单条已读、全部已读 |
| 🌐 多语言 | 简体中文 / English 一键切换，导航、标题、正文、按钮随语言实时更新，选择记忆于 `session` |

> 匿名用户浏览不产生任何登录门槛，适合分享给不注册的家人朋友查看。
> 站点默认按浏览器语言（`Accept-Language`）自动选择中文或英文，也可在导航栏右上角手动切换。

## 🌐 多语言支持

站点内置**简体中文 / English** 双语切换，所有可见文案（导航、页面标题、正文、按钮、表单提示、邮件与站内消息）都会随所选语言实时更新。

- **切换方式**：导航栏右上角的 `中文 / EN` 切换按钮，点击即跳转到当前页的对应语言版本；
- **记忆机制**：语言选择写入 `session`，刷新或再次访问仍保持；同时支持通过 URL `?lang=zh` / `?lang=en` 临时覆盖；
- **自动识别**：首次访问会根据浏览器 `Accept-Language` 自动选择中文或英文；
- **实现方式**：轻量字典式 i18n（`i18n.py`），无需 gettext 编译，对 Windows 友好，新增文案只需在字典中追加键值。

## 🧱 技术栈

- **后端**：Flask 3.x + SQLAlchemy 2.x（ORM）
- **数据库**：SQLite（零配置，单文件）
- **安全**：Flask-Login（会话）、Flask-Bcrypt（密码哈希）、Flask-WTF（**全站 CSRF 防护**）
- **邮件**：Flask-Mail（SMTP 验证码，QQ 邮箱开箱即用）
- **前端**：原生 HTML5 + CSS3 + JavaScript（响应式、深浅色友好，无重型依赖）

## 🚀 快速开始

### 环境要求

- Python 3.10+
- pip

### 安装与运行

```bash
# 1. 克隆项目
git clone https://github.com/DHJ999/mini_personal_blog.git
cd mini_personal_blog

# 2. 创建并激活虚拟环境（Windows）
python -m venv venv
venv\Scripts\activate        # Linux/macOS: source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 生成环境变量文件并编辑
#    Windows: copy .env.example .env
cp .env.example .env

# 5. 启动（开发模式）
python app.py
```

打开浏览器访问 **http://localhost:5000** 即可。

### 👤 首次管理员

启动时自动创建管理员，规则如下：

- 设置了环境变量 `ADMIN_USERNAME` / `ADMIN_PASSWORD`（推荐）→ 用你的账号；
- **未设置** 且以 `FLASK_DEBUG=1` 运行 → 兜底创建 `admin / admin123`（仅限本机调试）；
- 两者都未满足 → 不创建管理员，请直接注册普通用户。

> ⚠️ 生产环境务必显式配置 `ADMIN_*`，不要依赖 `admin/admin123`。

## ⚙️ 配置说明

所有敏感配置通过 `.env` / 环境变量注入，**严禁硬编码或提交 `.env` 到仓库**（已被 `.gitignore` 排除）。

| 变量 | 必填 | 说明 |
| --- | --- | --- |
| `SECRET_KEY` | ✅ 生产 | 会话签名密钥。用 `python -c "import secrets;print(secrets.token_hex(32))"` 生成 |
| `ADMIN_USERNAME` | 生产推荐 | 首次启动自动创建的管理员用户名 |
| `ADMIN_PASSWORD` | 生产推荐 | 管理员密码 |
| `ADMIN_EMAIL` | 选填 | 管理员邮箱（缺省为 `<用户名>@example.com`） |
| `MAIL_SERVER` | 注册/找回用 | SMTP 服务器，默认 `smtp.qq.com` |
| `MAIL_PORT` | 注册/找回用 | 默认 `465`（SSL） |
| `MAIL_USE_SSL` | 选填 | 默认 `1` |
| `MAIL_USERNAME` | 注册/找回用 | 发件邮箱（如 `xxx@qq.com`） |
| `MAIL_PASSWORD` | 注册/找回用 | **邮箱 SMTP 授权码**（非登录密码） |
| `FLASK_DEBUG` | 选填 | `1` 开启调试模式（**仅限本机**） |
| `HOST` / `PORT` | 选填 | 监听地址与端口，默认 `127.0.0.1:5000` |

> 未配置邮件时，注册 / 重置验证码会**打印到服务控制台**（仅限开发调试），并提示"验证码已发送"。

## 📂 项目结构

```
mini_personal_blog/
├── app.py                 # 主应用：路由、模型、业务逻辑
├── requirements.txt       # 依赖清单
├── .env.example           # 环境变量模板（复制为 .env 使用）
├── .gitignore             # 忽略 .env / venv / instance / uploads 等
├── static/
│   ├── style.css          # 全局样式
│   └── uploads/           # 上传图片（运行期产生，不入库）
├── instance/
│   └── blog.db            # SQLite 数据库（运行期产生，不入库）
└── templates/
    ├── base.html          # 布局骨架（导航 + 闪消息 + CSRF 注入）
    ├── index.html         # 首页（图片批次流）
    ├── image_detail.html  # 图片详情 + 评论区
    ├── image_batch.html   # 批次浏览 + 批次评论
    ├── login.html         # 登录
    ├── register.html      # 注册（邮箱验证码）
    ├── forgot_password.html # 找回密码（分步：邮箱 → 验证码 → 重置）
    ├── profile.html       # 个人中心（资料 / 头像）
    ├── messages.html      # 消息通知中心
    ├── admin.html         # 管理面板（图片管理）
    ├── admin_analytics.html # 数据统计看板
    ├── add_image.html     # 上传图片
    └── reply_item.html    # 回复组件（可复用）
```

## 🗺️ 路由一览

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/` | 首页图片流 | 公开 |
| GET | `/images/<batch_id>` | 按批次查看图片 | 公开 |
| GET/POST | `/image/<id>` | 图片详情 + 发表评论 | 评论需登录 |
| GET/POST | `/login` · `/register` · `/forgot_password` | 认证三件套 | 公开 |
| POST | `/logout` | 退出登录 | 登录 |
| GET/POST | `/profile` | 个人中心（含头像上传） | 登录 |
| GET | `/messages` | 消息通知 | 登录 |
| POST | `/mark_notification_read/<id>` · `/mark_all_notifications_read` | 标记已读 | 登录 |
| GET | `/admin` | 管理面板 | 管理员 |
| GET | `/admin/analytics` | 数据统计 | 管理员 |
| GET/POST | `/admin/add_image` | 上传图片 | 管理员 |
| POST | `/admin/delete_image/<id>` | 删除图片 | 管理员 |
| POST | `/comment_batch/<batch_id>` · `/reply_batch_comment/<batch_id>` · `/delete_comment/<comment_id>` | 评论 / 回复 / 删除 | 登录/管理员 |

## 🏭 生产部署

```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

上线前请务必检查：

- [ ] `FLASK_DEBUG=0`，使用 waitress / gunicorn 等正式 WSGI 服务器
- [ ] 设置随机的 `SECRET_KEY` 与强密码 `ADMIN_*`
- [ ] 配置真实 SMTP 邮箱授权码（否则验证码退化为控制台打印）
- [ ] 建议在 Nginx / Caddy 反向代理后提供 HTTPS 访问
- [ ] 定期备份 `instance/blog.db` 与 `static/uploads/`

## 🔒 安全设计

- **全站 CSRF 防护**：Flask-WTF 开启，每个 POST 表单自动注入 `csrf_token`，跨站伪造请求一律 400 拒绝
- **副作用仅 POST**：删除图片 / 删除评论 / 标记已读 / 登出均为 POST，杜绝"链接即操作"
- **敏感零入库**：`.env`、数据库、上传文件、`venv` 全部被 `.gitignore` 排除
- **密码安全**：bcrypt 加盐哈希存储；session 依赖 `SECRET_KEY` 签名
- **模板转义**：Jinja2 默认开启自动转义，防存储型 XSS
- **权限分层**：访客 / 登录用户 / 管理员三级，后台路由仅管理员可达

## 📝 License

本项目仅供学习交流使用。如需商用或二次分发，请自行补充许可证并注明出处。

---

<div align="center">

Made with ❤️ · [DHJ 的小站](https://github.com/DHJ999/mini_personal_blog)

📘 英文文档：[README_EN.md](README_EN.md)

</div>
