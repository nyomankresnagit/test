from flask import render_template
from app.dashboard import dashboard_bp
from flask_login import login_required
from flask_login import login_user, logout_user, login_required, current_user

# This function for Home / first view of the website

@dashboard_bp.route('/home')
@login_required
def dashboard():
    return render_template("dashboard/dashboard.html", username=current_user)