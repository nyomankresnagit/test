from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from app import db

def waktu_sekarang():
    now = datetime.now()
    return now

class member(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    idmember = db.Column(db.String(30), index=True, unique=True, nullable=False)
    nik = db.Column(db.String(16), nullable=False)
    nama = db.Column(db.String(99), nullable=False)
    jenis_kelamin = db.Column(db.String(10), nullable=False)
    alamat = db.Column(db.String(99), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=waktu_sekarang)
    created_by = db.Column(db.String(30), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.String(30), nullable=True)
    flag = db.Column(db.String(10), nullable=False, default='on')
     
    def __init__(self, idmember, nik, nama, jenis_kelamin, alamat, created_by):
        self.idmember = idmember
        self.nik = nik
        self.nama = nama
        self.jenis_kelamin = jenis_kelamin
        self.alamat = alamat
        self.created_by = created_by

    def __repr__(self):
        return '<buku %r>' % self.id

    def get_id(self):
        return str(self.id)