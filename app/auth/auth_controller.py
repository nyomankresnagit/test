from flask import *
from flask_login import login_user, logout_user, login_required, current_user
from app.auth.auth_model import auth
from app.dokter.dokter_model import dokter
from app.pasien.pasien_model import pasien
from app.admin.admin_model import admins
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, LoginManager
import datetime

def login():
    username = request.form.get("username")
    password = request.form.get("password")
    rows = auth.query.filter(auth.username==username).first()
    if not rows:
        flash("Username tidak tersedia.")
        return render_template("auth/login.html")
    elif not check_password_hash(rows.password, password):
        flash("Mohon Cek Username & Password dan coba lagi.")
        return render_template("auth/login.html")
    else:
        login_user(user=rows)
        return render_template("dashboard/dashboard.html", username=current_user)

def registerDokter():
    status = 'dokter'
    username = request.form.get("username")
    usernameDokter = request.form.get("username")
    password = request.form.get("password")
    nama_dokter = request.form.get("namaDokter")
    hari_kerja = request.form.get("hariKerja")
    jam_kerja = request.form.get("jamKerja")
    date = datetime.datetime.now()
    user = auth.query.filter(auth.username==username).first()
    if user:
        flash("Username sudah ada. Silahkan pilih username lain.")
    else:
        newUser = auth(username=username, status_auth=status, password=generate_password_hash(password, method='sha256'), flag="Y", created_date=date, updated_date=date)
        db.session.add(newUser)
        db.session.commit()
        newDokter = dokter(username=usernameDokter, password=password, nama_dokter=nama_dokter, hari_kerja=hari_kerja, jam_kerja=jam_kerja, status_pemeriksaan="N", flag="Y", created_date=date, updated_date=date)
        db.session.add(newDokter)
        db.session.commit()
        flash("User berhasil didaftarkan.")
    return render_template("auth/login.html")

def registerPasien():
    status = 'pasien'
    username = request.form.get("username")
    usernamePasien = request.form.get("username")
    password = request.form.get("password")
    nama_pasien = request.form.get("namaPasien")
    alamat_pasien = request.form.get("alamatPasien")
    date = datetime.datetime.now()
    user = auth.query.filter(auth.username==username).first()
    if user:
        flash("Username sudah ada. Silahkan pilih username lain.")
    else:
        newUser = auth(username=username, status_auth=status, password=generate_password_hash(password, method='sha256'), flag="Y", created_date=date, updated_date=date)
        db.session.add(newUser)
        db.session.commit()
        newPasien = pasien(username=usernamePasien, password=password, nama_pasien=nama_pasien, alamat_pasien=alamat_pasien, status_diperiksa="N", flag="Y", created_date=date, updated_date=date)
        db.session.add(newPasien)
        db.session.commit()
        flash("User berhasil didaftarkan.")
    return render_template("auth/login.html")

def registerAdmin():
    status = 'admin'
    username = request.form.get("username")
    usernameAdmin = request.form.get("username")
    password = request.form.get("password")
    nama_admin = request.form.get("namaAdmin")
    jabatan = request.form.get("jabatan")
    date = datetime.datetime.now()
    user = auth.query.filter(auth.username==username).first()
    if user:
        flash("Username sudah ada. Silahkan pilih username lain.")
    else:
        newUser = auth(username=username, status_auth=status, password=generate_password_hash(password, method='sha256'), flag="Y", created_date=date, updated_date=date)
        db.session.add(newUser)
        db.session.commit()
        id = findAuth(username)
        newAdmin = admin(id_auth=id, username=usernameAdmin, password=password, nama_admin=nama_admin, jabatan=jabatan, flag="Y", created_date=date, updated_date=date)
        db.session.add(newAdmin)
        db.session.commit()
        flash("Admin berhasil didaftarkan.")
    return render_template("auth/login.html")

def logout():
    logout_user()
    return render_template("auth/login.html")

def findAuth(username):
    find = auth.query.filter(auth.username==username).first()
    return find.id_auth