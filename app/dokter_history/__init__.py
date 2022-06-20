from flask import Blueprint

# Function Blueprint for connect dokter_history file / folder

dokter_history_bp = Blueprint('dokter_history_bp', __name__, template_folder='templates', static_folder='static')

from app.dokter_history import dokter_history_view