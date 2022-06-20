from flask import Blueprint

admin_history_bp = Blueprint('admin_history_bp',__name__, template_folder='templates', static_folder='static')

from app.admin_history import admin_history_view