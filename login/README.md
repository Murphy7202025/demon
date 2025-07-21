test
# Flask 简单登录页面

## 功能简介
本项目基于 Python 3.10 和 Flask 框架，实现了一个简单的用户登录页面，包含基础的权限验证和安全措施，便于后续扩展和集成。

---

## 1. 安全性
- **密码加密存储**：用户密码使用 `Werkzeug` 的 `generate_password_hash` 进行哈希存储，登录时用 `check_password_hash` 校验，避免明文密码泄露。
- **会话管理**：使用 Flask 的 `session` 管理用户登录状态，`secret_key` 随机生成，防止会话劫持。
- **防止XSS**：模板渲染采用 Flask 的 `render_template_string`，自动对用户输入进行转义，防止跨站脚本攻击。
- **防止CSRF**：如需更高安全性，可集成 Flask-WTF 等扩展实现 CSRF 防护。

## 2. 权限验证与角色机制
- **装饰器实现**：通过 `@authorize(modules, access)` 装饰器实现权限验证。可针对不同模块和操作粒度控制访问权限。
- **超级管理员机制**：支持超级管理员（superadmin），其邮箱在代码中配置，拥有所有权限。
- **用户-角色-权限结构**：用户信息、角色、权限均在代码中写死，便于演示和扩展。每个用户有邮箱、角色，角色对应不同模块的权限。
- **用法示例**：
  ```python
  @authorize('module1', 'read')
  def index():
      ...
  @authorize('module2', ['read', 'write'])
  def some_api():
      ...
  ```
- **灵活扩展**：如需增加模块、操作或角色，只需修改 `roles_permissions` 结构。

## 3. 性能与可扩展性
- **轻量高效**：Flask 本身为轻量级框架，适合小型应用和原型开发，后续可平滑迁移到更复杂的架构。
- **易于扩展**：用户数据、权限体系等均为模块化设计，后续可接入数据库（如MySQL、PostgreSQL）、缓存（如Redis）等。
- **会话可配置**：可根据实际部署环境，将 session 存储切换为 Redis、Memcached 等，提升性能和分布式能力。

## 4. 技术栈选择及理由
- **Python 3.10**：语法简洁，生态丰富，适合快速开发和维护。
- **Flask**：轻量、灵活、文档完善，适合中小型项目和原型开发。
- **Werkzeug**：Flask 的底层库，提供安全的密码哈希和校验方法。
- **依赖管理**：通过 `requirements.txt` 管理依赖，便于环境部署和迁移。

---

## 快速开始
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 运行项目：
   ```bash
   python app.py
   ```
3. 访问：
   浏览器打开 http://127.0.0.1:5000

---

## 账号与权限示例
- 用户名：admin  密码：admin123  角色：superadmin（邮箱：admin@example.com，拥有所有权限）
- 用户名：user   密码：user123   角色：user（邮箱：user@example.com，module1:read, module2:read/write）

## 超级管理员邮箱
- `admin@example.com`（可在 app.py 的 superadmin_emails 列表中配置） 
