from flask import *
from app.dokter.dokter_model import dokter
from app.auth.auth_model import auth
from app.dokter_history import dokter_history_controller
from app.trans.trans_model import trans
from app.auth import auth_controller
from app import db, pd, BytesIO
import datetime
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

# This file is work for setting the function

# The function below work for showing the active data on the database.
def viewDokter():
    rows = dokter.query.filter(dokter.flag=="Y").all()
    return render_template("dokter/dokter.html", datas=rows, username=current_user)

# The function below work for adding data to the database.
# This function use form to get value form the website.
def addDokter():
    username = request.form.get("username")
    password = request.form.get("password")
    nama_dokter = request.form.get("namaDokter")
    hari_kerja = request.form.get("hariKerja")
    jam_kerja = request.form.get("jamKerja")
    created_date = datetime.datetime.now()
    updated_date = datetime.datetime.now()
    newUser = auth(username=username, status_auth='dokter', password=generate_password_hash(password, method='sha256'), flag="Y", created_date=created_date, updated_date=updated_date)
    db.session.add(newUser)
    db.session.commit()
    id = auth_controller.findAuth(username)
    saveAdd = dokter(id_auth=id, kuota=5, username=username, password=password, nama_dokter=nama_dokter, hari_kerja=hari_kerja, jam_kerja=jam_kerja, created_date=created_date, updated_date=updated_date, flag="Y")
    db.session.add(saveAdd)
    db.session.commit()
    flash("Data Successfully Added.")
    return redirect(url_for('dokter_bp.viewDokter'))
    db.session.close()

# The function belom work for update / edit data on the database.
# This function use form to get value form the website.
def editDokter(uid):
    nama_dokter = request.form.get("namaDokter1")
    hari_kerja = request.form.get("hariKerja1")
    jam_kerja = request.form.get("jamKerja1")
    updated_date = datetime.datetime.now()
    data = checkDataDokter(uid)
    username = current_user.username
    if "Ada" == data:
        flash("Data Tidak Dapat Diupdate. Dokter sedang dalam transaksi.")
    else:
        saveEditDokter = dokter.query.filter(dokter.id_dokter==uid).first()
        dokter_history_controller.addDokterHistory(username, uid, saveEditDokter.nama_dokter, saveEditDokter.jam_kerja, saveEditDokter.hari_kerja, updated_date)
        saveEditDokter.nama_dokter = nama_dokter
        saveEditDokter.hari_kerja = hari_kerja
        saveEditDokter.jam_kerja = jam_kerja
        saveEditDokter.updated_date = updated_date
        saveEditDokter.username = username
        saveEditDokter.flag = "Y"
        db.session.commit()
        flash("Data Successfully Updated.")
    return redirect(url_for('dokter_bp.viewDokter'))
    db.session.close()

# The function below work for change flag and didnt deleting data from the database, just change flag from "Y" to "N"
# This function using data id from the website.
def deleteDokter(uid):
    status = checkDataDokter(uid)
    if "Ada" == status:
        flash("Data Tidak dapat Dihapus. Dokter sedang dalam transaksi.")
        return redirect(url_for('dokter_bp.viewDokter'))
    else:
        saveDelete = dokter.query.filter(dokter.id_dokter==uid).first()
        saveDelete.flag = "N"
        saveDelete.updated_date = datetime.datetime.now()
        db.session.commit()
        flash("Data Successfully Deleted.")
        return redirect(url_for('dokter_bp.viewDokter'))
        db.session.close()

# The function below work for searching data from the website and showing active data from database.
# This function using form to get value from the website.
def searchDokter():
    id_dokter = request.form.get("idDokter")
    nama_dokter = request.form.get("namaDokter")
    hari_kerja = request.form.get("hariKerja")
    jam_kerja = request.form.get("jamKerja")
    if id_dokter == "":
        id_dokter = "%"
    else:
        id_dokter = id_dokter
    if nama_dokter == "":
        nama_dokter = "%"
    else:
        nama_dokter = "%" + nama_dokter + "%"
    if jam_kerja == "":
        jam_kerja = "%"
    else:
        jam_kerja = "%" + jam_kerja + "%"
    if hari_kerja == "":
        hari_kerja = "%"
    else:
        hari_kerja = "%" + hari_kerja + "%"
    rows = dokter.query.filter(dokter.id_dokter.like(id_dokter), dokter.nama_dokter.like(nama_dokter), dokter.jam_kerja.like(jam_kerja), dokter.hari_kerja.like(hari_kerja), dokter.flag=="Y").all()
    return render_template("dokter/dokter.html", datas = rows, username=current_user)
    db.session.close()

# The function below work for import data from xlsx file and added data to the database.
# This function use xlsx file with predefined templates.
def importFileDokter():
    if request.method == 'POST':
        f = request.files['file']
        data_xls = pd.read_excel(f)
        created_date = datetime.datetime.now()
        updated_date = datetime.datetime.now()
        for i in range(len(data_xls)):
            nama_dokter = data_xls.loc[i][1]
            hari_kerja = data_xls.loc[i][2]
            jam_kerja = data_xls.loc[i][3]
            username = data_xls.loc[i][4]
            password = data_xls.loc[i][5]
            newUser = auth(username=username, status_auth='dokter', password=generate_password_hash(password, method='sha256'), flag="Y", created_date=created_date, updated_date=updated_date)
            db.session.add(newUser)
            db.session.commit()
            id = auth_controller.findAuth(username)
            saveAdd = dokter(id_auth=id, kuota=5, username=username, password=password, nama_dokter=nama_dokter, hari_kerja=hari_kerja, jam_kerja=jam_kerja, flag="Y", created_date=created_date, updated_date=updated_date)
            db.session.add(saveAdd)
            db.session.commit()
        return redirect(url_for('dokter_bp.viewDokter'))
    return render_template("dokter/dokter.html", username=current_user)

# The function below work for export template for adding data to the database.
# This function export xlsx file.
def downloadTemplateDokter():
    df_1 = pd.DataFrame(columns=['Nama Dokter', 'Hari Kerja', 'Jam Kerja', 'Username', 'Password',])
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df_1.to_excel(writer, sheet_name = "Sheet_1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]
    format = workbook.add_format()
    format.set_bg_color('#eeeeee')
    worksheet.set_column(0,2)
    writer.close()
    output.seek(0)
    return send_file(output, attachment_filename="Template_Dokter.xlsx", as_attachment=True)
    con.close()

# The function below work for checking data from the database that has specified id.
# When data showing value Y, the status changed into Ada therefore status changed into Tidak when data showing N value.
def checkDataDokter(uid):
    rows = dokter.query.filter(dokter.id_dokter==uid).first()
    if rows.status_pemeriksaan == "Y":
        status = "Ada"
    elif rows.status_pemeriksaan == "N":
        status = "Tidak"
    return status
