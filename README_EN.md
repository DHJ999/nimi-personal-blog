<div align="center">

# 🏠 DHJ's Blog

**A lightweight Flask-based personal blog** —— image sharing, comments & replies, and message notifications, ready to run out of the box.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Frontend](https://img.shields.io/badge/Frontend-HTML%20%2F%20CSS%20%2F%20JS-E34F26?logo=html5&logoColor=white)]()
[![CSRF](https://img.shields.io/badge/CSRF-Protected-success)]()
[![i18n](https://img.shields.io/badge/i18n-中文%20%2F%20EN-blue)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-ff69b4)]()

📘 **中文文档**：[README.md](README.md)

</div>

---

## 📖 Overview

A personal image-blog system built around **lightweight and private** sharing. Registered users can upload and share images; visitors and members can comment and reply, and each reply is delivered to the other party as a real-time in-site message. Admins get a dedicated analytics dashboard and a content-management panel.

Technically, a single `app.py` powers the entire application — ideal for learning full-stack Flask, or as a small family/friends photo-sharing album.

## ✨ Features

| Category | Feature |
| --- | --- |
| 📷 Image sharing | Single / batch uploads, grouped and displayed by batch (`uploads/` stored locally) |
| 💬 Comments | Image-detail comments and batch comment areas, with **multi-level replies** |
| 🔔 Notifications | Comments / replies automatically generate in-site messages, with an unread badge and "mark all read" |
| 🔐 Accounts | Email-verification registration, login, **forgot-password (email reset)**, bcrypt-hashed passwords |
| 👤 Profile | Edit display name / email / password, upload a custom avatar |
| 🛡️ Access control | Visitors may browse; commenting and the admin panel require login; admin-only panel |
| 📊 Analytics | Dashboard of visits, image count, comment count, message count, etc. (`/admin/analytics`) |
| ⚙️ Message mgmt | Comment / reply notification list, mark-one-read, mark-all-read |
| 🌐 i18n | One-click switch between Simplified Chinese / English; nav, titles, body and buttons update live, choice persisted in `session` |

> Anonymous browsing has no login barrier, making it easy to share with family and friends who don't want to register.
> The site auto-selects Chinese or English based on the browser's `Accept-Language` on first visit; you can also switch manually from the top-right of the navigation bar.

## 🌐 Multi-language Support

The site ships with **Simplified Chinese / English** bilingual switching. Every visible string (navigation, page titles, body text, buttons, form hints, emails and in-site messages) updates live with the selected language.

- **How to switch**: the `中文 / EN` toggle in the top-right of the navigation bar — clicking it jumps to the current page in the chosen language.
- **Persistence**: the language choice is written to `session` and survives refresh / revisits; you can also temporarily override via the URL `?lang=zh` / `?lang=en`.
- **Auto-detection**: first visit auto-selects Chinese or English from the browser's `Accept-Language`.
- **Implementation**: lightweight dictionary-based i18n (`i18n.py`) — no gettext compilation, Windows-friendly; adding new copy is just appending a key/value to the dictionary.

## 🧱 Tech Stack

- **Backend**: Flask 3.x + SQLAlchemy 2.x (ORM)
- **Database**: SQLite (zero-config, single file)
- **Security**: Flask-Login (sessions), Flask-Bcrypt (password hashing), Flask-WTF (**site-wide CSRF protection**)
- **Email**: Flask-Mail (SMTP verification codes, works out of the box with QQ Mail)
- **Frontend**: Plain HTML5 + CSS3 + JavaScript (responsive, light/dark friendly, no heavy dependencies)

## 🚀 Quick Start

### Requirements

- Python 3.10+
- pip

### Install & Run

```bash
# 1. Clone the project
git clone https://github.com/DHJ999/mini_personal_blog.git
cd mini_personal_blog

# 2. Create and activate a virtual environment (Windows)
python -m venv venv
venv\Scripts\activate        # Linux/macOS: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate the env file and edit it
cp .env.example .env

# 5. Start (development mode)
python app.py
```

Open **http://localhost:5000** in your browser.

### 👤 First-time Admin

An admin account is created automatically on startup according to these rules:

- If `ADMIN_USERNAME` / `ADMIN_PASSWORD` env vars are set (recommended) → your account is used;
- **Not set** and running with `FLASK_DEBUG=1` → a fallback `admin / admin123` is created (local debugging only);
- Neither satisfied → no admin is created; just register a normal user instead.

> ⚠️ In production, always configure `ADMIN_*` explicitly; do not rely on `admin/admin123`.

## ⚙️ Configuration

All sensitive configuration is injected via `.env` / environment variables. **Never hard-code secrets or commit `.env` to the repo** (it is excluded by `.gitignore`).

| Variable | Required | Description |
| --- | --- | --- |
| `SECRET_KEY` | ✅ Prod | Session-signing key. Generate with `python -c "import secrets;print(secrets.token_hex(32))"` |
| `ADMIN_USERNAME` | Rec. Prod | Admin username auto-created on first startup |
| `ADMIN_PASSWORD` | Rec. Prod | Admin password |
| `ADMIN_EMAIL` | Optional | Admin email (defaults to `<username>@example.com`) |
| `MAIL_SERVER` | Reg/reset | SMTP server, default `smtp.qq.com` |
| `MAIL_PORT` | Reg/reset | Default `465` (SSL) |
| `MAIL_USE_SSL` | Optional | Default `1` |
| `MAIL_USERNAME` | Reg/reset | Sender email (e.g. `xxx@qq.com`) |
| `MAIL_PASSWORD` | Reg/reset | **SMTP authorization code** (not the login password) |
| `FLASK_DEBUG` | Optional | `1` enables debug mode (**local only**) |
| `HOST` / `PORT` | Optional | Bind address and port, default `127.0.0.1:5000` |

> Without email configured, registration / reset codes are **printed to the server console** (development only), and the UI shows "code sent".

## 📂 Project Structure

```
mini_personal_blog/
├── app.py                 # Main app: routes, models, business logic
├── i18n.py                # Bilingual dictionary + translation helper
├── requirements.txt       # Dependency list
├── .env.example           # Env-var template (copy to .env)
├── .gitignore             # Ignores .env / venv / instance / uploads, etc.
├── static/
│   ├── style.css          # Global styles (incl. language-switch UI)
│   └── uploads/           # Uploaded images (runtime, not in repo)
├── instance/
│   └── blog.db            # SQLite database (runtime, not in repo)
└── templates/
    ├── base.html          # Layout skeleton (nav + flash + CSRF injection + lang switch)
    ├── index.html         # Home (image-batch feed)
    ├── image_detail.html  # Image detail + comments
    ├── image_batch.html   # Batch view + batch comments
    ├── login.html         # Login
    ├── register.html      # Register (email verification)
    ├── forgot_password.html # Forgot password (steps: email → code → reset)
    ├── profile.html       # Profile (info / avatar)
    ├── messages.html      # Notification center
    ├── admin.html         # Admin panel (image management)
    ├── admin_analytics.html # Analytics dashboard
    ├── add_image.html     # Upload images
    └── reply_item.html    # Reusable reply component
```

## 🗺️ Routes

| Method | Path | Description | Access |
| --- | --- | --- | --- |
| GET | `/` | Home image feed | Public |
| GET | `/images/<batch_id>` | View images by batch | Public |
| GET/POST | `/image/<id>` | Image detail + post comment | Comment needs login |
| GET/POST | `/login` · `/register` · `/forgot_password` | Auth trio | Public |
| POST | `/logout` | Log out | Login |
| GET/POST | `/profile` | Profile (incl. avatar upload) | Login |
| GET | `/messages` | Notifications | Login |
| POST | `/mark_notification_read/<id>` · `/mark_all_notifications_read` | Mark read | Login |
| GET | `/admin` | Admin panel | Admin |
| GET | `/admin/analytics` | Analytics | Admin |
| GET/POST | `/admin/add_image` | Upload images | Admin |
| POST | `/admin/delete_image/<id>` | Delete image | Admin |
| POST | `/comment_batch/<batch_id>` · `/reply_batch_comment/<batch_id>` · `/delete_comment/<comment_id>` | Comment / reply / delete | Login/Admin |
| GET | `/set_language/<lang>` | Switch language (zh/en), persists to session | Public |

## 🏭 Production Deployment

```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

Before going live, please check:

- [ ] `FLASK_DEBUG=0`, served by a real WSGI server (waitress / gunicorn)
- [ ] Random `SECRET_KEY` and strong `ADMIN_*` passwords set
- [ ] Real SMTP authorization code configured (otherwise codes degrade to console output)
- [ ] HTTPS recommended behind an Nginx / Caddy reverse proxy
- [ ] Regularly back up `instance/blog.db` and `static/uploads/`

## 🔒 Security Design

- **Site-wide CSRF protection**: Flask-WTF enabled; every POST form auto-injects `csrf_token`; cross-site forgery requests are rejected with 400.
- **Side effects are POST-only**: delete image / delete comment / mark read / logout are all POST — no "link is an action".
- **Nothing sensitive in the repo**: `.env`, database, uploads, and `venv` are all excluded by `.gitignore`.
- **Password safety**: bcrypt salted hashing; session signed by `SECRET_KEY`.
- **Template auto-escaping**: Jinja2 auto-escaping on by default, preventing stored XSS.
- **Layered access**: visitor / logged-in user / admin tiers; admin routes are admin-only.

## 📝 License

This project is open-sourced under the **MIT License** — see [LICENSE](LICENSE). Copyright © 2026 DHJ999.

MIT is a permissive license: anyone may freely use, modify, and redistribute the code (including commercially), with the sole obligation to preserve the copyright and permission notice. Third-party dependencies (Flask, etc.) and Cropper.js loaded via CDN remain under their respective original licenses.

---

<div align="center">

Made with ❤️ · [DHJ's Blog](https://github.com/DHJ999/mini_personal_blog)

📘 中文文档：[README.md](README.md)

</div>
