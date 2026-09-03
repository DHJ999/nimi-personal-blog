from flask import Flask, render_template, redirect, url_for, request, flash, g, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from flask_wtf import CSRFProtect
from datetime import datetime, timedelta, timezone
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from i18n import get_text
import os
import random
import secrets
import string
import uuid

load_dotenv()

app = Flask(__name__)
# 生产环境务必通过环境变量注入随机 SECRET_KEY，未设置时每次启动随机生成（重启后 session 失效）
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///blog.db'
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER') or 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
# 单次上传上限 20MB，防止超大文件打爆磁盘
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

# 邮件配置通过 .env / 环境变量提供，未配置时验证码降级为打印到控制台（仅限开发）
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 465))
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', '1') == '1'
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', '0') == '1'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME'] or None

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)
# 全站 CSRF 防护：所有 POST/PUT/DELETE 请求必须携带 csrf_token
csrf = CSRFProtect(app)

verification_codes = {}


def _t(key, **kwargs):
    """后端用：按当前请求语言取文案（flash / 通知 / 邮件等）。"""
    return get_text(getattr(g, 'lang', 'zh'), key, **kwargs)


@app.context_processor
def inject_i18n():
    """向所有模板注入 t() 与当前语言 lang。"""
    return {
        'lang': getattr(g, 'lang', 'zh'),
        't': lambda key, **kw: get_text(getattr(g, 'lang', 'zh'), key, **kw),
    }


def _utcnow():
    """返回不带时区的 UTC 当前时间（避免 datetime.utcnow 的弃用告警）"""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _mail_configured():
    return bool(os.environ.get('MAIL_USERNAME') and os.environ.get('MAIL_PASSWORD'))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    nickname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(200), nullable=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(200))
    date_uploaded = db.Column(db.DateTime, default=_utcnow)
    batch_id = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='image', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=_utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    is_reply = db.Column(db.Boolean, default=False)
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    date_posted = db.Column(db.DateTime, default=_utcnow)
    link = db.Column(db.String(200), nullable=True)

class VisitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), nullable=False)
    user_agent = db.Column(db.String(200), nullable=True)
    endpoint = db.Column(db.String(200), nullable=False)
    visit_time = db.Column(db.DateTime, default=_utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/set_language/<lang>')
def set_language(lang):
    """语言切换：写入 session 后跳回来源页（或首页）。"""
    if lang in ('zh', 'en'):
        session['lang'] = lang
    next_url = request.args.get('next') or request.referrer or url_for('index')
    return redirect(next_url)

@app.before_request
def before_request():
    # 语言解析优先级：URL ?lang= > session > 浏览器 Accept-Language > 中文
    req_lang = request.args.get('lang')
    if req_lang in ('zh', 'en'):
        session['lang'] = req_lang
    g.lang = session.get('lang') or (request.accept_languages.best_match(['zh', 'en']) or 'zh')

    g.unread_notifications = 0
    if current_user.is_authenticated:
        g.unread_notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    if request.endpoint and not request.endpoint.startswith('static'):
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip and ',' in ip:
            ip = ip.split(',')[0].strip()
        user_agent = request.headers.get('User-Agent', '')[:200]
        user_id = current_user.id if current_user.is_authenticated else None
        try:
            visit_log = VisitLog(
                ip_address=ip,
                user_agent=user_agent,
                endpoint=request.endpoint,
                user_id=user_id
            )
            db.session.add(visit_log)
            db.session.commit()
        except:
            pass

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_verification_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def _log_dev_code(email, code, purpose):
    """开发模式（未配置邮件）时把验证码打印到控制台"""
    print('=================================')
    print(f'[{_t("dev." + purpose)}] {_t("dev.header")}')
    print(f'邮箱: {email}')
    print(f'验证码: {code}')
    print('=================================')


def send_verification_email(email, code):
    """发送注册验证码邮件；未配置邮件时降级为控制台打印"""
    if not _mail_configured():
        _log_dev_code(email, code, 'register')
        return True
    msg = Message(_t('email.register_subject'),
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[email])
    msg.body = _t('email.register_body', code=code)
    try:
        mail.send(msg)
        print(f'注册验证码 {code} 已发送到邮箱 {email}')
        return True
    except Exception as e:
        print(f'邮件发送失败: {e}')
        _log_dev_code(email, code, '注册验证码')
        return True

@app.route('/')
def index():
    images = Image.query.order_by(Image.date_uploaded.desc()).all()
    image_batches = {}
    for image in images:
        if image.batch_id not in image_batches:
            image_batches[image.batch_id] = {
                'batch_id': image.batch_id,
                'images': [],
                'date_uploaded': image.date_uploaded
            }
        image_batches[image.batch_id]['images'].append(image)
        if image.date_uploaded > image_batches[image.batch_id]['date_uploaded']:
            image_batches[image.batch_id]['date_uploaded'] = image.date_uploaded
    
    # 过滤掉空批次
    batches_list = [batch for batch in image_batches.values() if batch['images']]
    batches_list.sort(key=lambda x: x['date_uploaded'], reverse=True)
    
    return render_template('index.html', image_batches=batches_list)

@app.route('/images/<batch_id>')
def image_batch(batch_id):
    images = Image.query.filter_by(batch_id=batch_id).order_by(Image.date_uploaded.desc()).all()
    if not images:
        return redirect(url_for('index'))
    return render_template('image_batch.html', images=images, batch_id=batch_id)

@app.route('/image/<int:id>', methods=['GET', 'POST'])
@login_required
def image_detail(id):
    image = db.get_or_404(Image, id)
    if request.method == 'POST':
        content = request.form.get('content', '')
        parent_id = request.form.get('parent_id', type=int)
        if content.strip():
            parent = None
            if parent_id:
                parent = db.session.get(Comment, parent_id)
                if parent is None or parent.image_id != image.id:
                    parent = None  # 非法父评论，按普通评论处理
            comment = Comment(content=content, user_id=current_user.id, image_id=id,
                              parent_id=parent.id if parent else None,
                              is_reply=bool(parent))
            db.session.add(comment)
            db.session.commit()
            if parent is not None and parent.user_id != current_user.id:
                db.session.add(Notification(
                    user_id=parent.user_id,
                    content=_t('notif.reply', name=current_user.nickname or current_user.username),
                    link=url_for('image_batch', batch_id=image.batch_id),
                ))
            elif image.user_id and image.user_id != current_user.id:
                db.session.add(Notification(
                    user_id=image.user_id,
                    content=_t('notif.comment', name=current_user.nickname or current_user.username),
                    link=url_for('image_batch', batch_id=image.batch_id),
                ))
            db.session.commit()
            flash(_t('flash.comment_posted'), 'success')
            return redirect(url_for('image_detail', id=id))
    return render_template('image_detail.html', image=image)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_or_email = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username_or_email).first()
        if not user:
            user = User.query.filter_by(email=username_or_email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin') if user.is_admin else url_for('index'))
        else:
            flash(_t('flash.login_failed'), 'danger')
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        nickname = request.form.get('nickname', '')
        
        # 处理裁剪后的头像
        cropped_data = request.form.get('cropped_data', '')
        if cropped_data:
            import base64
            from datetime import datetime
            
            # 解码 base64 图片数据
            img_data = cropped_data.split(',')[1]
            img_bytes = base64.b64decode(img_data)
            
            # 生成唯一文件名
            filename = f'avatar_{current_user.id}_{datetime.now().strftime("%Y%m%d%H%M%S")}.jpg'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # 保存文件
            with open(filepath, 'wb') as f:
                f.write(img_bytes)
            
            current_user.avatar = filename
        elif 'avatar' in request.files:
            # 处理传统文件上传
            file = request.files['avatar']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                current_user.avatar = filename
        
        if nickname:
            current_user.nickname = nickname
        
        db.session.commit()
        flash(_t('flash.account_updated'), 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/messages')
@login_required
def messages():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.date_posted.desc()).all()
    unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('messages.html', notifications=notifications, unread_count=unread_count)

@app.route('/mark_notification_read/<int:id>', methods=['POST'])
@login_required
def mark_notification_read(id):
    notification = db.get_or_404(Notification, id)
    if notification.user_id == current_user.id:
        notification.is_read = True
        db.session.commit()
    return redirect(notification.link or url_for('messages'))

@app.route('/mark_all_notifications_read', methods=['POST'])
@login_required
def mark_all_read():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).all()
    for notification in notifications:
        notification.is_read = True
    db.session.commit()
    return redirect(url_for('messages'))

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    
    images = Image.query.order_by(Image.date_uploaded.desc()).all()
    image_batches = {}
    for image in images:
        if image.batch_id not in image_batches:
            image_batches[image.batch_id] = {
                'images': [],
                'date_uploaded': image.date_uploaded
            }
        image_batches[image.batch_id]['images'].append(image)
        if image.date_uploaded > image_batches[image.batch_id]['date_uploaded']:
            image_batches[image.batch_id]['date_uploaded'] = image.date_uploaded
    
    # 过滤掉空批次
    batches_list = [batch for batch in image_batches.values() if batch['images']]
    batches_list.sort(key=lambda x: x['date_uploaded'], reverse=True)
    
    return render_template('admin.html', image_batches=batches_list)

@app.route('/admin/analytics')
@login_required
def admin_analytics():
    if not current_user.is_admin:
        return redirect(url_for('index'))

    from sqlalchemy import func
    today = _utcnow().date()
    week_ago = today - timedelta(days=7)

    total_visits = VisitLog.query.count()
    today_visits = VisitLog.query.filter(func.date(VisitLog.visit_time) == today).count()
    week_visits = VisitLog.query.filter(func.date(VisitLog.visit_time) >= week_ago).count()

    unique_ips = db.session.query(func.count(func.distinct(VisitLog.ip_address))).scalar()

    daily_stats = db.session.query(
        func.date(VisitLog.visit_time).label('date'),
        func.count(VisitLog.id).label('count')
    ).group_by(func.date(VisitLog.visit_time)).order_by(func.date(VisitLog.visit_time).desc()).limit(30).all()

    top_ips = db.session.query(
        VisitLog.ip_address,
        func.count(VisitLog.id).label('count')
    ).group_by(VisitLog.ip_address).order_by(func.count(VisitLog.id).desc()).limit(20).all()

    top_pages = db.session.query(
        VisitLog.endpoint,
        func.count(VisitLog.id).label('count')
    ).group_by(VisitLog.endpoint).order_by(func.count(VisitLog.id).desc()).limit(10).all()

    recent_visits = VisitLog.query.order_by(VisitLog.visit_time.desc()).limit(50).all()

    return render_template('admin_analytics.html',
                         total_visits=total_visits,
                         today_visits=today_visits,
                         week_visits=week_visits,
                         unique_ips=unique_ips,
                         daily_stats=daily_stats,
                         top_ips=top_ips,
                         top_pages=top_pages,
                         recent_visits=recent_visits)

@app.route('/admin/add_image', methods=['GET', 'POST'])
@login_required
def add_image():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    if request.method == 'POST':
        if 'files' not in request.files:
            flash(_t('flash.no_file'))
            return redirect(request.url)
        files = request.files.getlist('files')
        if not files or all(f.filename == '' for f in files):
            flash(_t('flash.no_file'))
            return redirect(request.url)
        caption = request.form.get('caption', '')
        batch_id = str(uuid.uuid4())
        uploaded_count = 0
        for file in files:
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = Image(filename=filename, caption=caption, batch_id=batch_id, user_id=current_user.id)
                db.session.add(image)
                uploaded_count += 1
        db.session.commit()
        flash(_t('flash.uploaded', count=uploaded_count), 'success')
        return redirect(url_for('admin'))
    return render_template('add_image.html')

@app.route('/admin/delete_image/<int:id>', methods=['POST'])
@login_required
def delete_image(id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    image = db.get_or_404(Image, id)
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
    except:
        pass
    db.session.delete(image)
    db.session.commit()
    flash(_t('flash.image_deleted'), 'success')
    return redirect(url_for('admin'))

@app.route('/comment_batch/<batch_id>', methods=['POST'])
@login_required
def comment_batch(batch_id):
    content = request.form['content']
    images = Image.query.filter_by(batch_id=batch_id).all()
    if images:
        comment = Comment(content=content, user_id=current_user.id, image_id=images[0].id)
        db.session.add(comment)
        db.session.commit()
        
        if images[0].user_id and images[0].user_id != current_user.id:
            notification = Notification(
                user_id=images[0].user_id,
                content=_t('notif.comment', name=current_user.nickname or current_user.username),
                link=url_for('image_batch', batch_id=batch_id),
            )
            db.session.add(notification)
            db.session.commit()
        
        flash(_t('flash.comment_success'))
    return redirect(url_for('image_batch', batch_id=batch_id))

@app.route('/reply_batch_comment/<batch_id>', methods=['POST'])
@login_required
def reply_batch_comment(batch_id):
    content = request.form['content']
    parent_id = request.form['parent_id']
    
    parent_comment = db.session.get(Comment, parent_id)
    if parent_comment:
        comment = Comment(content=content, user_id=current_user.id, image_id=parent_comment.image_id, parent_id=parent_id, is_reply=True)
        db.session.add(comment)
        db.session.commit()
        
        if parent_comment.user_id != current_user.id:
            notification = Notification(
                user_id=parent_comment.user_id,
                content=_t('notif.reply', name=current_user.nickname or current_user.username),
                link=url_for('image_batch', batch_id=batch_id),
            )
            db.session.add(notification)
            db.session.commit()
        
        image = db.session.get(Image, parent_comment.image_id)
        if image and image.user_id and image.user_id != current_user.id and image.user_id != parent_comment.user_id:
            notification = Notification(
                user_id=image.user_id,
                content=_t('notif.reply_image', name=current_user.nickname or current_user.username),
                link=url_for('image_batch', batch_id=batch_id),
            )
            db.session.add(notification)
            db.session.commit()
        
        flash(_t('flash.reply_success'))
    return redirect(url_for('image_batch', batch_id=batch_id))

@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = db.get_or_404(Comment, comment_id)
    
    if not current_user.is_admin and current_user.id != comment.author.id:
        flash(_t('flash.no_permission'), 'danger')
        return redirect(request.referrer or url_for('index'))
    
    def delete_comment_with_replies(comment):
        for reply in comment.replies:
            delete_comment_with_replies(reply)
        db.session.delete(comment)
    
    delete_comment_with_replies(comment)
    db.session.commit()
    flash(_t('flash.comment_deleted'))
    
    return redirect(request.referrer or url_for('index'))

@app.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    email = request.form.get('email')
    if not email:
        return {'success': False, 'message': _t('flash.email_required')}
    if User.query.filter_by(email=email).first():
        return {'success': False, 'message': _t('flash.email_registered')}
    code = generate_verification_code()
    verification_codes[email] = {
        'code': code,
        'expire': datetime.now() + timedelta(minutes=5)
    }
    if send_verification_email(email, code):
        return {'success': True, 'message': _t('flash.code_sent')}
    else:
        return {'success': False, 'message': _t('flash.email_send_failed')}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        nickname = request.form.get('nickname', '').strip()
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        code = request.form['verification_code']
        if not nickname:
            flash(_t('flash.enter_nickname'), 'danger')
            return render_template('register.html')
        if password != password_confirm:
            flash(_t('flash.password_mismatch'), 'danger')
            return render_template('register.html')
        if email not in verification_codes:
            flash(_t('flash.get_code_first'), 'danger')
            return render_template('register.html')
        code_info = verification_codes[email]
        if datetime.now() > code_info['expire']:
            flash(_t('flash.code_expired'), 'danger')
            del verification_codes[email]
            return render_template('register.html')
        if code != code_info['code']:
            flash(_t('flash.code_error'), 'danger')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash(_t('flash.email_registered'), 'danger')
            return render_template('register.html')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=email, nickname=nickname, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        del verification_codes[email]
        flash(_t('flash.register_success'), 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/send_reset_code', methods=['POST'])
def send_reset_code():
    email = request.form.get('email')
    if not email:
        return {'success': False, 'message': _t('flash.email_required')}
    user = User.query.filter_by(email=email).first()
    if not user:
        return {'success': False, 'message': _t('flash.email_unregistered')}
    code = generate_verification_code()
    verification_codes[email] = {
        'code': code,
        'expire': datetime.now() + timedelta(minutes=5)
    }
    if _mail_configured():
        msg = Message(_t('email.reset_subject'),
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email])
        msg.body = _t('email.reset_body', code=code)
        try:
            mail.send(msg)
            print(f'重置密码验证码 {code} 已发送到邮箱 {email}')
            return {'success': True, 'message': _t('flash.code_sent')}
        except Exception as e:
            print(f'邮件发送失败: {e}')
        _log_dev_code(email, code, 'reset')
    return {'success': True, 'message': _t('flash.code_sent')}

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    step = 'verify'
    email = ''
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'verify':
            email = request.form['email']
            code = request.form['verification_code']
            if email not in verification_codes:
                flash(_t('flash.get_code_first'), 'danger')
                return render_template('forgot_password.html', step='verify', email=email)
            code_info = verification_codes[email]
            if datetime.now() > code_info['expire']:
                flash(_t('flash.code_expired'), 'danger')
                del verification_codes[email]
                return render_template('forgot_password.html', step='verify', email=email)
            if code != code_info['code']:
                flash(_t('flash.code_error'), 'danger')
                return render_template('forgot_password.html', step='verify', email=email)
            step = 'reset'
        elif action == 'reset':
            email = request.form['email']
            password = request.form['password']
            password_confirm = request.form['password_confirm']
            if password != password_confirm:
                flash(_t('flash.password_mismatch'), 'danger')
                return render_template('forgot_password.html', step='reset', email=email)
            user = User.query.filter_by(email=email).first()
            if user:
                user.password = bcrypt.generate_password_hash(password).decode('utf-8')
                db.session.commit()
                del verification_codes[email]
                flash(_t('flash.reset_success'), 'success')
                return redirect(url_for('login'))
    return render_template('forgot_password.html', step=step, email=email)

@app.template_filter('beijing_time')
def beijing_time_filter(dt, format='%Y-%m-%d %H:%M'):
    if dt is None:
        return ''
    beijing_tz = timezone(timedelta(hours=8))
    dt_beijing = dt.replace(tzinfo=timezone.utc).astimezone(beijing_tz)
    return dt_beijing.strftime(format)

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    with app.app_context():
        db.create_all()
        admin_username = os.environ.get('ADMIN_USERNAME', '')
        admin_password = os.environ.get('ADMIN_PASSWORD', '')
        admin_email = os.environ.get('ADMIN_EMAIL', '')
        if not admin_username:
            # 开发模式兜底：FLASK_DEBUG=1 且没有管理员时创建 admin/admin123（仅限本机调试）
            if debug_mode and not User.query.filter_by(username='admin').first():
                admin_username, admin_password, admin_email = 'admin', 'admin123', 'admin@example.com'
        if admin_username and admin_password:
            if not User.query.filter_by(username=admin_username).first():
                hashed_pw = bcrypt.generate_password_hash(admin_password).decode('utf-8')
                db.session.add(User(
                    username=admin_username,
                    email=admin_email or f'{admin_username}@example.com',
                    password=hashed_pw,
                    is_admin=True,
                ))
                db.session.commit()
                if debug_mode:
                    print(f'[dev] 已创建管理员 {admin_username}（密码 {admin_password}），生产环境请通过环境变量 ADMIN_USERNAME/ADMIN_PASSWORD 设置')
    # 生产部署请使用 waitress/gunicorn，勿以 debug 模式对外服务
    app.run(
        host=os.environ.get('HOST', '127.0.0.1'),
        port=int(os.environ.get('PORT', 5000)),
        debug=debug_mode,
    )