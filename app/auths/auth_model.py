from flask_sqlalchemy import SQLAlchemy
from app import db

# MODEL TABEL admin
class admin(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(99), nullable=False)
    nama = db.Column(db.String(99), nullable=False)

    # PARAMETER INPUT
    def __init__(self, username, password, nama):
        self.username = username
        self.password = password
        self.nama = nama

    def __repr__(self):
        return '<admin %r>' % self.id


    