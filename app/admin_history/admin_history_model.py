from flask_sqlalchemy import SQLAlchemy
from app.admin.admin_model import admins
from app import db

# This file work for define and initialize model for the database.

class admin_history(db.Model):
    id_admin_history = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_admin = db.Column(db.Integer, db.ForeignKey('admins.id_admin'))
    username = db.Column(db.String(99), nullable=False)
    nama_admin = db.Column(db.String(80), nullable=False)
    jabatan = db.Column(db.String(80), nullable=False)
    flag = db.Column(db.String(2), nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, id_admin, nama_admin, username, jabatan, flag, created_date, updated_date):
        self.id_admin = id_admin
        self.nama_admin = nama_admin
        self.username = username
        self.jabatan = jabatan
        self.flag = flag
        self.created_date = created_date
        self.updated_date = updated_date
    
    def __repr__(self):
        return '<admin_history %r>' % self.id_admin_history