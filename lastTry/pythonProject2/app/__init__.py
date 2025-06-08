from flask import Flask


def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-here'
    # 注册 posts 蓝图
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    from .teacher import teacher_bp
    app.register_blueprint(teacher_bp)


    return app
