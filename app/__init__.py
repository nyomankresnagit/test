from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import DevelopmentConfig
import os
import pandas as pd
from io import BytesIO
from pathlib import Path
from flask_mysqldb import MySQL

# This file work for initialize projects that will run on the website.

# This code work for calling library Flask-SQLAlchemy to use the function inside that library.
db = SQLAlchemy()

# This code work for calling library Flask-Migrate to use the function inside that library.
migrate = Migrate()

# The code below work for running main app with Flask framework using configuration from file config.py.
# This code also register the blueprint from other folder / file.
def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    mysql = MySQL(app)
    mysql.app = app

    db.init_app(app)
    db.app = app

    migrate.init_app(app, db)
    migrate.app = app

    login_manager = LoginManager()
    login_manager.init_app(app)

    from app.auth.auth_model import auth
    @login_manager.user_loader
    def load_user(id_auth):
        return auth.query.get(int(id_auth))

    from app.auths import bp_auth as auths
    app.register_blueprint(auths)

    from app.buku import bp_buku as buku
    app.register_blueprint(buku)

    from app.member import bp_member as member
    app.register_blueprint(member)

    from app.transaksi import bp_transaksi as transaksi
    app.register_blueprint(transaksi)

    from app.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.admin_history import admin_history_bp
    app.register_blueprint(admin_history_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.dokter import dokter_bp
    app.register_blueprint(dokter_bp)

    from app.dokter_history import dokter_history_bp
    app.register_blueprint(dokter_history_bp)

    from app.pasien import pasien_bp
    app.register_blueprint(pasien_bp)

    from app.pasien_history import pasien_history_bp
    app.register_blueprint(pasien_history_bp)

    from app.trans import trans_bp
    app.register_blueprint(trans_bp)

    app.add_url_rule('/', endpoint='index')

    return app