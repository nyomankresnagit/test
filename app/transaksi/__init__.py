from flask import Blueprint

bp_transaksi = Blueprint('transaksi', __name__, template_folder='templates', static_folder='static')

from app.transaksi import transaksi_view