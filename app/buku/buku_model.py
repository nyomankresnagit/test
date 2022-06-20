from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from app import db

# FUNGSI MENDAPATKAN VARIABEL WAKTU SEKARANG
def waktu_sekarang():
    now = datetime.now()
    return now

# MODEL TABEL buku
class buku(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    kodebuku = db.Column(db.String(30), index=True, unique=True, nullable=False)
    judul = db.Column(db.String(99), nullable=False)
    genre = db.Column(db.String(30), nullable=False)
    lokasi = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=waktu_sekarang)
    created_by = db.Column(db.String(30), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.String(30), nullable=True)
    flag = db.Column(db.String(10), nullable=False, default='on')
     
    def __init__(self, kodebuku, judul, genre, lokasi, status, created_by):
        self.kodebuku = kodebuku
        self.judul = judul
        self.genre = genre
        self.lokasi = lokasi
        self.status = status
        self.created_by = created_by

    def __repr__(self):
        return '<buku %r>' % self.id

    def get_id(self):
        return str(self.id)