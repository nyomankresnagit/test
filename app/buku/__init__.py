from flask import Blueprint

bp_buku = Blueprint('buku', __name__, template_folder='templates', static_folder='static')

from app.buku import buku_view