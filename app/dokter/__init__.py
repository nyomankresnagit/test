from flask import Blueprint

# Function Blueprint for connect dokter file / folder

dokter_bp = Blueprint('dokter_bp', __name__, template_folder='templates', static_folder='static')

from app.dokter import dokter_view