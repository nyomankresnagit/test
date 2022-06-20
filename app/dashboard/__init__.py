from flask import Blueprint

# Function Blueprint for connect dashboard file / folder

dashboard_bp = Blueprint('dashboard_bp', __name__, template_folder='templates', static_folder='static')

from app.dashboard.view import dashboard