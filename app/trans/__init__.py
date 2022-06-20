from flask import Blueprint

# Function Blueprint for connect dokter_history file / folder

trans_bp = Blueprint('trans_bp', __name__, template_folder='templates', static_folder='static')

from app.trans import trans_view