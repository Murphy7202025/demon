from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 用户信息
users = {
    'admin': {
        'password': generate_password_hash('admin123'),
        'email': 'admin@example.com',
        'role': 'superadmin'
    },
    'user': {
        'password': generate_password_hash('user123'),
        'email': 'user@example.com',
        'role': 'user'
    }
}

# 角色权限
roles_permissions = {
    'superadmin': {'all': ['all']},  # 超级管理员拥有所有权限
    'user': {
        'module1': ['read'],
        'module2': ['read', 'write']
    }
}

# superadmin邮箱
superadmin_emails = ['admin@example.com']

from functools import lru_cache
from flask import abort

# 权限判断相关函数

def has_access_for_role(modules, accesses, role):
    """
    判断指定角色是否有指定模块的指定权限。
    :param modules: 模块名（字符串或列表）
    :param accesses: 权限（字符串或列表）
    :param role: 角色名
    """
    if isinstance(modules, list):
        role_module_access = []
        for m in modules:
            role_module_access += roles_permissions.get(role, {}).get(m, [])
    else:
        role_module_access = roles_permissions.get(role, {}).get(modules, [])
    if isinstance(accesses, list):
        return any(a in role_module_access for a in accesses)
    else:
        return accesses in role_module_access

@lru_cache(maxsize=100)
def is_super_admin(email):
    """
    判断当前用户是否为超级管理员。
    """
    return email in superadmin_emails

# 权限装饰器
def authorize(modules, access):
    """
    装饰器：只有当前用户拥有指定模块和权限时才允许访问。
    :param modules: 模块名
    :param access: 权限名或权限列表
    """
    def authorize_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'username' not in session:
                flash('请先登录！')
                return redirect(url_for('login'))
            user = users.get(session['username'])
            if not user:
                abort(403)
            # 超级管理员直接放行
            if is_super_admin(user['email']):
                return f(*args, **kwargs)
            # 普通权限判断
            if not has_access_for_role(modules, access, user['role']):
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return authorize_decorator

# 替换原有@login_required为@authorize
@app.route('/')
@authorize('module1', 'read')
def index():
    return f"欢迎, {session['username']}! <a href='/logout'>退出</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误')
    return render_template_string('''
        <h2>登录</h2>
        <form method="post">
            用户名: <input type="text" name="username"><br>
            密码: <input type="password" name="password"><br>
            <input type="submit" value="登录">
        </form>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul>
            {% for message in messages %}
              <li>{{ message }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
    ''')

@app.route('/logout')
@authorize('module1', 'read')
def logout():
    session.pop('username', None)
    flash('已退出登录')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True) 