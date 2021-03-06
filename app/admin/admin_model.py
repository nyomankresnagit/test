from flask_sqlalchemy import SQLAlchemy
from app.auth.auth_model import auth
from app import db

# This file work for define and initialize model for the database.

class admins(db.Model):
    id_admin = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_auth = db.Column(db.Integer, db.ForeignKey('auth.id_auth'))
    username = db.Column(db.String(99), nullable=False)
    password = db.Column(db.String(99), nullable=False)
    nama_admin = db.Column(db.String(80), nullable=False)
    jabatan = db.Column(db.String(80), nullable=False)
    flag = db.Column(db.String(2), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, id_auth, nama_admin, username, password, jabatan, flag, created_date, updated_date):
        self.id_auth = id_auth
        self.nama_admin = nama_admin
        self.username = username
        self.password = password
        self.jabatan = jabatan
        self.flag = flag
        self.created_date = created_date
        self.updated_date = updated_date
    
    def __repr__(self):
        return '<admin %r>' % self.id_admin