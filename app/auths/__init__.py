from flask import Blueprint

bp_auth = Blueprint('auths', __name__, template_folder='templates', static_folder='static')

from app.auths import auth_view