from flask import Blueprint

teacher_bp = Blueprint('teacher', __name__,template_folder='../../templates',url_prefix='/teacher')
from . import routes