from flask import Blueprint

bp_member = Blueprint('member', __name__, template_folder='templates', static_folder='static')

from app.member import member_view