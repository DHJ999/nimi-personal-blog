# -*- coding: utf-8 -*-
"""轻量级 i18n：纯字典实现，无需 gettext / 编译 .po 文件（Windows 友好）。

两种语言：zh（简体中文，默认）/ en（English）。
模板中通过全局函数 t('key', **kwargs) 调用；后端 flash / 通知 / 邮件通过 _t() 调用。
"""


TRANSLATIONS = {
    'zh': {
        # 站点
        'site_name': 'DHJ的小站',
        'footer': '© 2026 DHJ的小站. Made with ❤️ For you for me',

        # 导航
        'nav.home': '首页',
        'nav.me': '我',
        'nav.account': '👤 账户',
        'nav.messages': '📩 消息',
        'nav.logout': '🚪 退出登录',
        'nav.admin': '管理面板',
        'nav.login': '登录',
        'nav.register': '注册',

        # 语言切换
        'lang.zh': '中文',
        'lang.en': 'EN',

        # 首页
        'index.title': '一天又一天',
        'index.cover_alt': '封面图片',
        'index.no_images': '暂无图片',

        # 登录
        'login.title': '登录',
        'login.email': '邮箱',
        'login.email_ph': '请输入邮箱地址',
        'login.password': '密码',
        'login.password_ph': '请输入密码',
        'login.forgot': '忘记密码？',
        'login.submit': '登录',
        'login.no_account': '还没有账号？',
        'login.signup': '立即注册',

        # 注册
        'register.title': '注册',
        'register.nickname': '昵称',
        'register.nickname_ph': '请输入昵称',
        'register.email': '邮箱',
        'register.email_ph': '请输入邮箱地址',
        'register.password': '密码',
        'register.password_ph': '4-20位字母或数字',
        'register.password_hint': '密码长度4-20位，仅限字母和数字',
        'register.confirm': '确认密码',
        'register.confirm_ph': '请再次输入密码',
        'register.code': '验证码',
        'register.code_ph': '请输入验证码',
        'register.get_code': '获取验证码',
        'register.submit': '注册',
        'register.has_account': '已有账号？',
        'register.login': '立即登录',

        # 忘记密码
        'forgot.title': '忘记密码',
        'forgot.email': '邮箱',
        'forgot.email_ph': '请输入注册时的邮箱',
        'forgot.code': '验证码',
        'forgot.code_ph': '请输入验证码',
        'forgot.send': '发送验证码',
        'forgot.verify': '验证身份',
        'forgot.new_password': '新密码',
        'forgot.new_password_ph': '请输入新密码',
        'forgot.confirm': '确认密码',
        'forgot.confirm_ph': '请再次输入新密码',
        'forgot.reset': '重置密码',
        'forgot.back': '返回登录',

        # 个人中心
        'profile.title': '账户设置',
        'profile.avatar': '头像',
        'profile.nickname': '昵称',
        'profile.nickname_ph': '请输入昵称',
        'profile.email': '邮箱',
        'profile.type': '用户类型',
        'profile.author': '作者',
        'profile.user': '普通用户',
        'profile.save': '保存修改',
        'profile.crop_title': '选择头像区域',
        'profile.crop_confirm': '确认裁剪',
        'profile.crop_cancel': '取消',
        'profile.cropped': '✓ 头像已选择',

        # 消息中心
        'messages.title': '📩 我的消息',
        'messages.unread_count': '你有 {n} 条未读消息',
        'messages.tab_unread': '未读消息',
        'messages.tab_read': '已读消息',
        'messages.mark_all': '全部已读',
        'messages.badge_unread': '未读',
        'messages.badge_read': '已读',
        'messages.view': '查看详情 →',
        'messages.no_unread': '暂无未读消息',
        'messages.no_read': '暂无已读消息',
        'messages.back': '返回首页',

        # 管理面板
        'admin.title': '管理面板',
        'admin.upload': '上传新图片',
        'admin.stats': '📊 数据统计',
        'admin.daily': '日常管理',
        'admin.uploaded': '上传时间：',
        'admin.count': '{n} 张',
        'admin.date_format': '%Y年%m月%d日 %H:%M',
        'admin.view': '查看',
        'admin.delete': '删除',
        'admin.no_images': '暂无图片',

        # 数据统计
        'analytics.title': '📊 数据统计',
        'analytics.back': '返回管理面板',
        'analytics.total_visits': '总访问量',
        'analytics.today': '今日访问',
        'analytics.week': '本周访问',
        'analytics.unique_ip': '独立IP',
        'analytics.daily': '📈 每日访问统计（近30天）',
        'analytics.date': '日期',
        'analytics.visits': '访问量',
        'analytics.top_pages': '🏆 热门页面',
        'analytics.page': '页面',
        'analytics.ip_rank': '🌐 访问IP排行',
        'analytics.rank': '排名',
        'analytics.ip': 'IP地址',
        'analytics.visits_count': '访问次数',
        'analytics.recent': '🕐 最近访问记录',
        'analytics.time': '时间',
        'analytics.page_col': '访问页面',
        'analytics.user': '用户',
        'analytics.guest': '未登录',

        # 上传图片
        'add.title': '上传图片',
        'add.files': '选择图片（可多选）',
        'add.formats': '支持 JPG、PNG、GIF 格式',
        'add.preview_empty': '点击上方选择图片，或拖拽图片到此处',
        'add.caption': '图片说明（可选，所有图片共用）',
        'add.caption_ph': '为所有图片添加共同说明，可以换行输入',
        'add.submit': '上传',
        'add.cancel': '取消',

        # 图片详情
        'detail.back': '← 返回首页',
        'detail.comments': '评论 ({n})',
        'detail.author': '作者',
        'detail.reply': '回复',
        'detail.reply_ph': '写下你的回复...',
        'detail.send': '发送',
        'detail.cancel': '取消',
        'detail.comment_ph': '写下你的评论...',
        'detail.post': '发表评论',
        'detail.login_hint': '请先登录后发表评论',
        'detail.replied': '回复',

        # 图片批次
        'batch.back': '← 返回首页',
        'batch.images_count': '{n} 张图片',
        'batch.click_view': '点击查看大图',
        'batch.comments': '评论',
        'batch.comment_ph': '写下你的评论...',
        'batch.post_comment': '发送评论',
        'batch.login_hint': '请先登录后再评论',
        'batch.author': '作者',
        'batch.reply': '回复',
        'batch.delete': '删除',
        'batch.reply_ph': '写下你的回复...',
        'batch.send': '发送',
        'batch.cancel': '取消',
        'batch.no_comments': '暂无评论',
        'batch.lightbox_hint': '点击或按 ESC 关闭',
        'batch.large_alt': '大图',
        'batch.image_alt': '图片',
        'batch.date_format': '%Y年%m月%d日 %H:%M',

        # 回复组件
        'reply.author': '作者',
        'reply.reply': '回复',
        'reply.delete': '删除',
        'reply.reply_ph': '写下你的回复...',
        'reply.send': '发送',
        'reply.cancel': '取消',

        # 前端 JS 提示
        'js.enter_nickname': '请输入昵称',
        'js.enter_email': '请输入邮箱地址',
        'js.invalid_email': '请输入有效的邮箱地址',
        'js.enter_password': '请输入密码',
        'js.password_format': '密码长度需4-20位，仅限字母和数字',
        'js.enter_confirm': '请输入确认密码',
        'js.password_mismatch': '两次输入的密码不一致',
        'js.send_failed': '发送失败，请稍后重试',
        'js.sending': '发送中...',
        'js.retry_after': '秒后重试',
        'js.get_code_btn': '获取验证码',
        'js.enter_email_first': '请先输入邮箱地址',
        'js.send_code_btn': '发送验证码',
        'js.crop_first': '请先选择并裁剪头像区域',
        'js.delete_image_confirm': '确定删除这张图片？此操作不可恢复。',
        'js.delete_failed': '删除失败，请重试',
        'js.delete_comment_confirm': '确定要删除这条评论吗？所有回复也会被删除。',

        # 闪消息（flash）
        'flash.comment_posted': '评论已发布',
        'flash.login_failed': '登录失败，请检查用户名/邮箱和密码',
        'flash.account_updated': '账户信息已更新',
        'flash.no_file': '没有选择文件',
        'flash.uploaded': '{count} 张图片上传成功',
        'flash.image_deleted': '图片已删除',
        'flash.comment_success': '评论成功',
        'flash.reply_success': '回复成功',
        'flash.no_permission': '无权删除此评论',
        'flash.comment_deleted': '评论已删除',
        'flash.enter_nickname': '请输入昵称',
        'flash.password_mismatch': '两次输入的密码不一致',
        'flash.get_code_first': '请先获取验证码',
        'flash.code_expired': '验证码已过期，请重新获取',
        'flash.code_error': '验证码错误',
        'flash.email_registered': '该邮箱已被注册',
        'flash.register_success': '注册成功，请登录',
        'flash.reset_success': '密码重置成功，请登录',
        'flash.email_required': '请输入邮箱',
        'flash.email_unregistered': '该邮箱未注册',
        'flash.code_sent': '验证码已发送，请查收邮箱',
        'flash.email_send_failed': '邮件发送失败，请稍后重试',

        # 站内通知
        'notif.reply': '{name} 回复了你的评论',
        'notif.comment': '{name} 在你的图片下发表了评论',
        'notif.reply_image': '{name} 在你的图片评论下进行了回复',

        # 邮件
        'email.register_subject': 'DHJ的小站 - 注册验证码',
        'email.register_body': '你的注册验证码是：{code}\n\n验证码有效期为5分钟，请尽快使用。',
        'email.reset_subject': 'DHJ的小站 - 密码重置验证码',
        'email.reset_body': '你的密码重置验证码是：{code}\n\n验证码有效期为5分钟，请尽快使用。',

        # 开发模式控制台
        'dev.register': '注册验证码',
        'dev.reset': '密码重置验证码',
        'dev.header': '开发模式，未配置邮件，验证码如下：',
    },

    'en': {
        # Site
        'site_name': "DHJ's Blog",
        'footer': "© 2026 DHJ's Blog. Made with ❤️ For you for me",

        # Nav
        'nav.home': 'Home',
        'nav.me': 'Me',
        'nav.account': '👤 Account',
        'nav.messages': '📩 Messages',
        'nav.logout': '🚪 Log out',
        'nav.admin': 'Admin',
        'nav.login': 'Log in',
        'nav.register': 'Sign up',

        # Language
        'lang.zh': '中文',
        'lang.en': 'EN',

        # Home
        'index.title': 'Day by Day',
        'index.cover_alt': 'Cover image',
        'index.no_images': 'No images yet',

        # Login
        'login.title': 'Log in',
        'login.email': 'Email',
        'login.email_ph': 'Enter your email',
        'login.password': 'Password',
        'login.password_ph': 'Enter your password',
        'login.forgot': 'Forgot password?',
        'login.submit': 'Log in',
        'login.no_account': 'No account yet?',
        'login.signup': 'Sign up now',

        # Register
        'register.title': 'Sign up',
        'register.nickname': 'Nickname',
        'register.nickname_ph': 'Enter your nickname',
        'register.email': 'Email',
        'register.email_ph': 'Enter your email',
        'register.password': 'Password',
        'register.password_ph': '4-20 letters or digits',
        'register.password_hint': '4-20 characters, letters or digits only',
        'register.confirm': 'Confirm password',
        'register.confirm_ph': 'Re-enter your password',
        'register.code': 'Verification code',
        'register.code_ph': 'Enter the code',
        'register.get_code': 'Get code',
        'register.submit': 'Sign up',
        'register.has_account': 'Already have an account?',
        'register.login': 'Log in',

        # Forgot password
        'forgot.title': 'Forgot password',
        'forgot.email': 'Email',
        'forgot.email_ph': 'Enter your registered email',
        'forgot.code': 'Verification code',
        'forgot.code_ph': 'Enter the code',
        'forgot.send': 'Send code',
        'forgot.verify': 'Verify',
        'forgot.new_password': 'New password',
        'forgot.new_password_ph': 'Enter new password',
        'forgot.confirm': 'Confirm password',
        'forgot.confirm_ph': 'Re-enter new password',
        'forgot.reset': 'Reset password',
        'forgot.back': 'Back to login',

        # Profile
        'profile.title': 'Account settings',
        'profile.avatar': 'Avatar',
        'profile.nickname': 'Nickname',
        'profile.nickname_ph': 'Enter your nickname',
        'profile.email': 'Email',
        'profile.type': 'Account type',
        'profile.author': 'Author',
        'profile.user': 'Regular user',
        'profile.save': 'Save changes',
        'profile.crop_title': 'Select avatar area',
        'profile.crop_confirm': 'Confirm crop',
        'profile.crop_cancel': 'Cancel',
        'profile.cropped': '✓ Avatar selected',

        # Messages
        'messages.title': '📩 My messages',
        'messages.unread_count': 'You have {n} unread message(s)',
        'messages.tab_unread': 'Unread',
        'messages.tab_read': 'Read',
        'messages.mark_all': 'Mark all read',
        'messages.badge_unread': 'Unread',
        'messages.badge_read': 'Read',
        'messages.view': 'View details →',
        'messages.no_unread': 'No unread messages',
        'messages.no_read': 'No read messages',
        'messages.back': 'Back to home',

        # Admin
        'admin.title': 'Admin panel',
        'admin.upload': 'Upload images',
        'admin.stats': '📊 Statistics',
        'admin.daily': 'Daily management',
        'admin.uploaded': 'Uploaded: ',
        'admin.count': '{n} images',
        'admin.date_format': '%Y-%m-%d %H:%M',
        'admin.view': 'View',
        'admin.delete': 'Delete',
        'admin.no_images': 'No images',

        # Analytics
        'analytics.title': '📊 Statistics',
        'analytics.back': 'Back to admin',
        'analytics.total_visits': 'Total visits',
        'analytics.today': "Today's visits",
        'analytics.week': "This week's visits",
        'analytics.unique_ip': 'Unique IPs',
        'analytics.daily': '📈 Daily visits (last 30 days)',
        'analytics.date': 'Date',
        'analytics.visits': 'Visits',
        'analytics.top_pages': '🏆 Top pages',
        'analytics.page': 'Page',
        'analytics.ip_rank': '🌐 Visitor IP ranking',
        'analytics.rank': 'Rank',
        'analytics.ip': 'IP Address',
        'analytics.visits_count': 'Visits',
        'analytics.recent': '🕐 Recent visits',
        'analytics.time': 'Time',
        'analytics.page_col': 'Page',
        'analytics.user': 'User',
        'analytics.guest': 'Guest',

        # Upload
        'add.title': 'Upload images',
        'add.files': 'Select images (multiple)',
        'add.formats': 'JPG, PNG, GIF supported',
        'add.preview_empty': 'Click above to select, or drag images here',
        'add.caption': 'Caption (optional, shared by all)',
        'add.caption_ph': 'Add a shared caption for all images (multi-line)',
        'add.submit': 'Upload',
        'add.cancel': 'Cancel',

        # Image detail
        'detail.back': '← Back to home',
        'detail.comments': 'Comments ({n})',
        'detail.author': 'Author',
        'detail.reply': 'Reply',
        'detail.reply_ph': 'Write your reply...',
        'detail.send': 'Send',
        'detail.cancel': 'Cancel',
        'detail.comment_ph': 'Write your comment...',
        'detail.post': 'Post comment',
        'detail.login_hint': 'Please log in to comment',
        'detail.replied': 'replied',

        # Image batch
        'batch.back': '← Back to home',
        'batch.images_count': '{n} images',
        'batch.click_view': 'Click to view',
        'batch.comments': 'Comments',
        'batch.comment_ph': 'Write your comment...',
        'batch.post_comment': 'Post comment',
        'batch.login_hint': 'Please log in to comment',
        'batch.author': 'Author',
        'batch.reply': 'Reply',
        'batch.delete': 'Delete',
        'batch.reply_ph': 'Write your reply...',
        'batch.send': 'Send',
        'batch.cancel': 'Cancel',
        'batch.no_comments': 'No comments yet',
        'batch.lightbox_hint': 'Click or press ESC to close',
        'batch.large_alt': 'Large image',
        'batch.image_alt': 'Image',
        'batch.date_format': '%Y-%m-%d %H:%M',

        # Reply item
        'reply.author': 'Author',
        'reply.reply': 'Reply',
        'reply.delete': 'Delete',
        'reply.reply_ph': 'Write your reply...',
        'reply.send': 'Send',
        'reply.cancel': 'Cancel',

        # JS prompts
        'js.enter_nickname': 'Please enter your nickname',
        'js.enter_email': 'Please enter your email',
        'js.invalid_email': 'Please enter a valid email',
        'js.enter_password': 'Please enter your password',
        'js.password_format': 'Password must be 4-20 letters or digits',
        'js.enter_confirm': 'Please confirm your password',
        'js.password_mismatch': 'Passwords do not match',
        'js.send_failed': 'Failed to send. Please try again.',
        'js.sending': 'Sending...',
        'js.retry_after': 's',
        'js.get_code_btn': 'Get code',
        'js.enter_email_first': 'Please enter your email first',
        'js.send_code_btn': 'Send code',
        'js.crop_first': 'Please select and crop your avatar',
        'js.delete_image_confirm': 'Delete this image? This cannot be undone.',
        'js.delete_failed': 'Failed to delete. Please try again.',
        'js.delete_comment_confirm': 'Delete this comment? All replies will be removed too.',

        # Flash
        'flash.comment_posted': 'Comment posted',
        'flash.login_failed': 'Login failed. Check your username/email and password',
        'flash.account_updated': 'Account updated',
        'flash.no_file': 'No file selected',
        'flash.uploaded': '{count} images uploaded',
        'flash.image_deleted': 'Image deleted',
        'flash.comment_success': 'Comment posted',
        'flash.reply_success': 'Reply posted',
        'flash.no_permission': 'You are not allowed to delete this comment',
        'flash.comment_deleted': 'Comment deleted',
        'flash.enter_nickname': 'Please enter your nickname',
        'flash.password_mismatch': 'Passwords do not match',
        'flash.get_code_first': 'Please get the code first',
        'flash.code_expired': 'Code expired, please get a new one',
        'flash.code_error': 'Incorrect code',
        'flash.email_registered': 'This email is already registered',
        'flash.register_success': 'Registration successful, please log in',
        'flash.reset_success': 'Password reset successful, please log in',
        'flash.email_required': 'Please enter your email',
        'flash.email_unregistered': 'This email is not registered',
        'flash.code_sent': 'Code sent, please check your email',
        'flash.email_send_failed': 'Failed to send email, please try again',

        # Notifications
        'notif.reply': '{name} replied to your comment',
        'notif.comment': '{name} commented on your photo',
        'notif.reply_image': '{name} replied to a comment on your photo',

        # Email
        'email.register_subject': "DHJ's Blog - Registration code",
        'email.register_body': 'Your registration code is: {code}\n\nThe code is valid for 5 minutes.',
        'email.reset_subject': "DHJ's Blog - Password reset code",
        'email.reset_body': 'Your password reset code is: {code}\n\nThe code is valid for 5 minutes.',

        # Dev console
        'dev.register': 'Registration code',
        'dev.reset': 'Password reset code',
        'dev.header': '[DEV] Email not configured. Verification code:',
    },
}


def get_text(lang, key, **kwargs):
    """按语言取文案；缺失时回退中文，再回退 key 本身，保证永不报 KeyError。"""
    table = TRANSLATIONS.get(lang, TRANSLATIONS['zh'])
    text = table.get(key, TRANSLATIONS['zh'].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text
