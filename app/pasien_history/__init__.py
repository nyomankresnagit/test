from flask import Blueprint

# Function Blueprint for connect dokter_history file / folder

pasien_history_bp = Blueprint('pasien_history_bp', __name__, template_folder='templates', static_folder='static')

from app.pasien_history import pasien_history_view