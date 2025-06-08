from flask import Blueprint

auth_bp = Blueprint('auth', __name__,template_folder='../../templates')
# 导入路由模块（放在末尾避免循环导入）
from . import routes#当 Python 执行到这行代码时，会自动加载 routes.py 文件，并将其中定义的
# 路由（如 @posts_bp.route）与蓝图对象（如 posts_bp）关联起来。