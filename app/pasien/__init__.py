from flask import Blueprint

# Function Blueprint for connect dokter_history file / folder

pasien_bp = Blueprint('pasien_bp',__name__, template_folder='templates', static_folder='static')

from app.pasien import pasien_view