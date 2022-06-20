from app import db
from flask import *
from app.admin.admin_model import admins
from app.admin_history import admin_history_controller
from app.auth.auth_model import auth
from app.auth import auth_controller
import datetime
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

def viewAdmin():
    rows = db.session.query(admins).join(auth).filter(auth.status_auth=="admin").all()
    return render_template("admin/admin.html", datas=rows, username=current_user)

def addAdmin():
    username = request.form.get("username")
    password = request.form.get("password")
    nama_admin = request.form.get("namaAdmin")
    jabatan = request.form.get("jabatan")
    date = datetime.datetime.now()
    newUser = auth(username=username, status_auth='admin', password=generate_password_hash(password, method='sha256'), flag="Y", created_date=date, updated_date=date)
    db.session.add(newUser)
    db.session.commit()
    id = auth_controller.findAuth(username)
    saveAdd = admins(id_auth=id, username=username, password=password, nama_admin=nama_admin, jabatan=jabatan, flag="Y", created_date=date, updated_date=date)
    db.session.add(saveAdd)
    db.session.commit()
    return redirect(url_for('admin_bp.viewAdmin'))
    db.session.close()

def deleteAdmin(idAdmin):
    saveDelete = admins.query.filter(admins.id_admin==idAdmin).first()
    saveDelete.flag = "N"
    saveDelete.updated_date = datetime.datetime.now()
    db.session.commit()
    flash("Data Successfully Deleted.")
    return redirect(url_for('admin_bp.viewAdmin'))
    db.session.close()

def editAdmin(idAdmin):
    nama_admin = request.form.get("namaAdmin")
    jabatan = request.form.get("jabatan")
    updated_date = datetime.datetime.now()
    saveEditAdmin = admins.query.filter(admin.id_admin==idAdmin).first()
    admin_history_controller.addAdminHistory(idAdmin, saveEditAdmin.nama_admin, saveEditAdmin.jabatan, updated_date)
    saveEditAdmin.nama_admin = nama_admin
    saveEditAdmin.jabatan = jabatan
    saveEditAdmin.updated_date = updated_date
    saveEditAdmin.flag = "Y"
    db.session.commit()
    flash("Data Successfully Updated.")
    return redirect(url_for('admin_bp.viewAdmin'))
    db.session.close()

def searchAdmin():
    id_admin = request.form.get("idAdmin")
    namaAdmin = request.form.get("namaAdmin")
    if id_admin == "":
        id_admin = "%"
    else:
        id_admin = id_admin
    if nama_admin == "":
        nama_admin = "%"
    else:
        nama_admin = "%" + nama_admin + "%"
    rows = admins.query.filter(admins.id_admin.like(id_admin), admins.nama_admin.like(nama_admin), admins.flag=="Y").all()
    return render_template("admin/admin.html", datas = rows, username=current_user)
    db.session.close()