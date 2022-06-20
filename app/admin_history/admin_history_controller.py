from app import db
from flask import *
from app.admin_history.admin_history_model import admin_history
import datetime

def viewAdminHistory():
    rows = admin_history.query.filter(admin_history.flag=="Y").all()
    return render_template("admin_history/admin_history.html")

def addAdminHistory(idAdmin, nama_admin, jabatan, updated_date):
    saveAdd = admin_history(id_admin=idAdmin, nama_admin=nama_admin, jabatan=jabatan, updated_date=updated_date)
    db.session.add(saveAdd)
    db.session.commit()
    return redirect(url_for('admin_bp.viewAdmin'))
    db.session.close()