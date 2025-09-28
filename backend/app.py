from flask import Flask, redirect, url_for, session
from flask_cors import CORS
from jinja2 import ChoiceLoader, FileSystemLoader
import os

# -------------------------
# 建立 Flask app
# -------------------------
app = Flask(
    __name__,
    static_folder='../frontend/static',
    template_folder='../frontend/templates'
)

# secret_key 與檔案設定
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# CORS
CORS(app, supports_credentials=True)

# -------------------------
# Jinja2 載入前台 + 管理員模板
# -------------------------
app.jinja_loader = ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader('../admin_frontend/templates')
])

# -------------------------
# 載入 Blueprint
# -------------------------
from auth import auth_bp
from company import company_bp
from resume import resume_bp
from admin import admin_bp
from users import users_bp
from notification import notification_bp
from preferences import preferences_bp

# 註冊 Blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(company_bp)
app.register_blueprint(resume_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(users_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(preferences_bp)

# -------------------------
# 首頁路由（使用者前台）
# -------------------------
@app.route("/")
def index():
    if "username" in session and session.get("role") == "student":
        return redirect(url_for("users_bp.student_home")) 
    return redirect(url_for("auth_bp.login_page"))

# -------------------------
# 管理員首頁（後台）
# -------------------------
@app.route("/admin")
def admin_index():
    if "username" in session and session.get("role") == "admin":
        return redirect(url_for("admin_bp.admin_home"))
    return redirect(url_for("auth_bp.login_page"))

# -------------------------
# 主程式入口
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
