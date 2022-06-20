from flask_login import login_required
from flask import render_template
from app.auth import auth_bp, auth_controller, auth_model

@auth_bp.route('/homelogin')
def formLogin():
    return render_template("auth/login.html")

@auth_bp.route('/login', methods=['POST'])
def login():
    return auth_controller.login()

@auth_bp.route('/registerDokter', methods=['POST'])
def registerDokter():
    return auth_controller.registerDokter()

@auth_bp.route('/registerPasien', methods=['POST'])
def registerPasien():
    return auth_controller.registerPasien()

@auth_bp.route('/registerAdmin', methods=['POST'])
def registerAdmin():
    return auth_controller.registerAdmin()

@auth_bp.route('/logout')
@login_required
def logout():
    return auth_controller.logout()