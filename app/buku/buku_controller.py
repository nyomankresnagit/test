from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for, make_response, send_file
)
import os, csv, time
from os.path import join, dirname, realpath
from werkzeug.exceptions import abort
from datetime import datetime, timedelta
from io import StringIO
from app import db
from app.buku.buku_model import buku

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(realpath(__file__))))
FOLDER_CSVBUKU = os.path.join(BASEDIR, './static/csvupload/buku/')
########################## CEKLIS #######################
# Tambah buku = CLEAR
# download format buku = CLEAR
# upload buku = CLEAR
# display buku = CLEAR 
# search buku = CLEAR 
# download buku = CLEAR
# update buku ada = CLEAR
# update buku dipinjam = CLEAR
# delete buku = CLEAR

# FUNGSI GENERATE 6 DIGIT ANGKA RANDOM UNTUK KODE BUKU
def random():
    import random, math
    digits = [i for i in range(0,10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random()*10)
        random_str += str(digits[index])
    return random_str

# FUNGSI MENAMPILKAN DATA BUKU
def databuku():
    while True:
        generate_id = random()
        cekid = db.session.query(buku.kodebuku).filter_by(kodebuku=generate_id).first()
        if not cekid:
            break
    
    bukus = searchbuku()[0]
    ci = searchbuku()[1]
    cj = searchbuku()[2]
    cg = searchbuku()[3]
    cp = searchbuku()[4]
    ca = searchbuku()[5]
    return render_template('buku/databuku.html', generate_id=generate_id, bukus=bukus, ci=ci, cj=cj, cg=cg, cp=cp, ca=ca)

# FUNGSI MENAMBAHKAN DATA BUKU
def tambahbuku():
    if request.method == 'POST':
        if 'tambahbuku' in request.form:
            kodebuku = request.form['kodebuku']
            judul = request.form['judul']
            genre = request.form['genre']
            lokasi = request.form['lokasi']
            status = request.form['status']
            created_by = request.form['created_by']
            lenkodebuku = len(kodebuku)
            cekbuku = db.session.query(buku.kodebuku).filter_by(kodebuku=kodebuku).first()
            messagebuku = ''
            if lenkodebuku == 6:
                if not kodebuku:
                    messagebuku = 'Masukkan Kode Buku'
                elif not judul:
                    messagebuku = 'Masukkan Judul Buku'
                elif not genre:
                    messagebuku = 'Masukkan Genre Buku'
                elif not lokasi:
                    messagebuku = 'Tulis Lokasi Rak Buku'
                elif cekbuku:
                    messagebuku = 'Kode Buku Sudah Terpakai'
                
                if not messagebuku:
                    insertData = buku(kodebuku=kodebuku, judul=judul, genre=genre, lokasi=lokasi, status=status, created_by=created_by)
                    db.session.add(insertData)
                    db.session.commit()
                    flash('BERHASIL MENAMBAHKAN BUKU', category="flash-ok")
                    return redirect(url_for('buku.databuku'))
                    db.session.close()
            else:
                messagebuku = 'KODE BUKU HARUS 6 DIGIT'

    flash(messagebuku, category="flash-error")
    return redirect(url_for('buku.databuku'))

# FUNGSI PENCARIAN BUKU
def searchbuku(): 
    ci = cj = cg = cp = ca = ''
    bukusearch = []
    bukusearch = db.session.query(buku.id, buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.status=="ada", buku.flag=="on").all()
    if request.method == 'POST': 
        if 'caridatabuku' in request.form:
            carikodebuku  = ci = request.form['carikodebuku']
            carijudul = cj = request.form['carijudul']
            carigenre = cg = request.form['carigenre']
            caripinjam = cp = request.form.get('caripinjam')
            cariada = ca = request.form.get('cariada')
            ci = cj = cg = p = "%"
            ci += str(carikodebuku)
            ci += p
            cj += str(carijudul)
            cj += p
            cg += str(carigenre)
            cg += p

            if not cp and not ca:
                bukusearch = db.session.query(buku.id, buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.flag=="on").all()
            elif not cp and ca:
                bukusearch = db.session.query(buku.id, buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.status==ca, buku.flag=="on").all()
            elif cp and not ca:
                bukusearch = db.session.query(buku.id, buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.status==cp, buku.flag=="on").all()
            elif cp and ca:
                bukusearch = db.session.query(buku.id, buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.flag=="on").all()
    return bukusearch, ci, cj, cg, cp, ca
    db.session.close()

# FUNGSI MENAMBAHKAN DATA BUKU MENGGUNAKAN CSV
def uploadbuku():
    kodebuku = kodebukuin = judul = genre = lokasi = ''
    statusada = "ada"
    statusdipinjam = "dipinjam"
    flag = "updated"
    skipkosong = 0
    skipdigit = 0
    if request.method == 'POST':

        if 'uploaddatabuku' in request.form:
            filebuku = request.files['filebuku']
            created_by = request.form['created_by']
            updated_by = request.form['updated_by']
            if filebuku.filename != '':
                #set_filename (waktu upload_nama file)
                timefilename = datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y_%H.%M.%S..%f_')
                timefilename += filebuku.filename
                #cursor path ke static/files
                filepath = os.path.join(FOLDER_CSVBUKU, timefilename)
                #save file on path static/files
                filebuku.save(filepath)
                #CEK FORMAT
                with open(filepath) as file:
                    csv_filebukulen = csv.reader(file)
                    length = len(list(csv_filebukulen)[0])
                    if length == 4:
                        #CEK PENAMAAN
                        with open(filepath) as file:
                            csv_filebukuhead = csv.reader(file)
                            kodebuku, judul, genre, lokasi = list(csv_filebukuhead)[0]
                            if kodebuku == 'KODE BUKU' and judul == 'JUDUL BUKU' and genre == 'GENRE' and lokasi == 'LOKASI':
                                #PROSES UPLOAD
                                with open(filepath) as file:
                                    csv_filebuku = csv.reader(file)
                                    next(csv_filebuku)
                                    for row in csv_filebuku:
                                        kodebuku = list(row)[0]
                                        judul = list(row)[1]
                                        genre = list(row)[2]
                                        lokasi = list(row)[3]
                                        lenkodebukucsv = len(kodebuku)
                                        if kodebuku and judul and genre and lokasi:
                                            if lenkodebukucsv == 6:
                                                datasama = db.session.query(buku.kodebuku).filter_by(kodebuku=kodebuku).first()
                                                if datasama:
                                                    datadipinjam = db.session.query(buku.kodebuku).filter_by(status='dipinjam').first()
                                                    if datadipinjam:
                                                        kodebukuin = db.session.query(buku.kodebuku).filter_by(kodebuku=kodebuku).first()[0]
                                                        kodebukuold = kodebukuio = str(db.session.query(buku.kodebuku).filter_by(kodebuku=kodebukuin).first()[0])
                                                        judulold = str(db.session.query(buku.judul).filter_by(kodebuku=kodebukuin).first()[0])
                                                        genreold = str(db.session.query(buku.genre).filter_by(kodebuku=kodebukuin).first()[0])
                                                        lokasiold = str(db.session.query(buku.lokasi).filter_by(kodebuku=kodebukuin).first()[0])
                                                        strold = "_updated_"
                                                        epoch = str(time.time())
                                                        kodebukuold += strold
                                                        kodebukuold += epoch
                                                        updateData = buku.query.filter_by(kodebuku=kodebukuin).first()
                                                        updateData.kodebuku = kodebukuold
                                                        updateData.judul = judulold
                                                        updateData.genre = genreold
                                                        updateData.lokasi = lokasiold
                                                        updateData.updated_at = datetime.now()
                                                        updateData.updated_by = updated_by
                                                        updateData.flag = flag
                                                        db.session.commit()
                                                        insertData = buku(kodebuku=kodebukuio, judul=judulold, genre=genreold, lokasi=lokasi, status=statusdipinjam, created_by=created_by)
                                                        db.session.add(insertData)
                                                        db.session.commit()
                                                    elif not datadipinjam:
                                                        kodebukuin = db.session.query(buku.kodebuku).filter_by(kodebuku=kodebuku).first()[0]
                                                        kodebukuold = kodebukuio = str(db.session.query(buku.kodebuku).filter_by(kodebuku=kodebukuin).first()[0])
                                                        judulold = str(db.session.query(buku.judul).filter_by(kodebuku=kodebukuin).first()[0])
                                                        genreold = str(db.session.query(buku.genre).filter_by(kodebuku=kodebukuin).first()[0])
                                                        lokasiold = str(db.session.query(buku.lokasi).filter_by(kodebuku=kodebukuin).first()[0])
                                                        strold = "_updated_"
                                                        epoch = str(time.time())
                                                        kodebukuold += strold
                                                        kodebukuold += epoch
                                                        updateData = buku.query.filter_by(kodebuku=kodebukuin).first()
                                                        updateData.kodebuku = kodebukuold
                                                        updateData.judul = judulold
                                                        updateData.genre = genreold
                                                        updateData.lokasi = lokasiold
                                                        updateData.updated_at = datetime.now()
                                                        updateData.updated_by = updated_by
                                                        updateData.flag = flag
                                                        db.session.commit()
                                                        insertData = buku(kodebuku=kodebuku, judul=judul, genre=genre, lokasi=lokasi, status=statusada, created_by=created_by)
                                                        db.session.add(insertData)
                                                        db.session.commit()
                                                elif not datasama:
                                                    insertData = buku(kodebuku=kodebuku, judul=judul, genre=genre, lokasi=lokasi, status=statusada, created_by=created_by)
                                                    db.session.add(insertData)
                                                    db.session.commit()
                                            else:
                                                skipdigit = skipdigit + 1
                                        else:
                                            skipkosong = skipkosong + 1
                            else:
                                flash('GAGAL MENGUPLOAD, COBA CEK KEMBALI PENAMAANNYA', category="flash-error")
                                return redirect(url_for('buku.databuku'))
                                db.session.close()
                    else:
                        flash('GAGAL MENGUPLOAD, COBA CEK KEMBALI FORMATNYA', category="flash-error")
                        return redirect(url_for('buku.databuku'))
                        db.session.close()
    
    flash('BERHASIL MENGUPLOAD DATA BUKU', category="flash-ok")
    if skipkosong == 0 and skipdigit == 0:
        flash('DATA YANG TERSKIP = '+str(skipkosong)+' DATA ADA YANG KOSONG, '+str(skipdigit)+' DATA DENGAN KODE BUKU TIDAK 6 DIGIT', category="flash-ok")
    else:
        flash('DATA YANG TERSKIP = '+str(skipkosong)+' DATA ADA YANG KOSONG, '+str(skipdigit)+' DATA DENGAN KODE BUKU TIDAK 6 DIGIT', category="flash-error")
    return redirect(url_for('buku.databuku'))
    db.session.close()

# FUNGSI MENDAPATKAN DATA BUKU BERDASARKAN ID
def get_buku(id): 
    getbuku = buku.query.filter_by(id=id).first()

    if getbuku is None:
        abort(404, f"buku dengan id {id} tidak ditemukan")

    return getbuku

# FUNGSI MENGEDIT BUKU YANG MASIH TERSEDIA
def updatebukuada(id): 
    getbuku = get_buku(id)
    kodebukuold = str(db.session.query(buku.kodebuku).filter_by(id=id).first()[0])
    judulold = str(db.session.query(buku.judul).filter_by(id=id).first()[0])
    genreold = str(db.session.query(buku.genre).filter_by(id=id).first()[0])
    lokasiold = str(db.session.query(buku.lokasi).filter_by(id=id).first()[0])
    strold = "_updated_"
    epoch = str(time.time())
    kodebukuold += strold
    kodebukuold += epoch
    if request.method == 'POST':
        kodebuku = request.form['kodebuku']
        judul = request.form['judul']
        genre = request.form['genre']
        lokasi = request.form['lokasi']
        status = request.form['status']
        flag = request.form['flag']
        created_by = request.form['created_by']
        updated_by = request.form['updated_by']
        messagebuku = ''
        if not kodebuku:
            messagebuku = 'Masukkan Kode Buku'
        elif not judul:
            messagebuku = 'Masukkan Judul Buku'
        elif not genre:
            messagebuku = 'Masukkan Genre Buku'
        elif not lokasi:
            messagebuku = 'Tulis Lokasi Rak Buku'
            
        if not messagebuku:
            updateData = buku.query.filter_by(id=id).first()
            updateData.kodebuku = kodebukuold
            updateData.judul = judulold
            updateData.genre = genreold
            updateData.lokasi = lokasiold
            updateData.updated_at = datetime.now()
            updateData.updated_by = updated_by
            updateData.flag = flag
            db.session.commit()
            insertData = buku(kodebuku=kodebuku, judul=judul, genre=genre, lokasi=lokasi, status=status, created_by=created_by)
            db.session.add(insertData)
            db.session.commit()
            flash('BERHASIL MENGEDIT DATA BUKU', category="flash-ok")
            return redirect(url_for('buku.databuku'))
            db.session.close()
        else:
            flash(messagebuku, category="flash-error")
        
    return render_template('buku/updatebukuada.html', getbuku=getbuku)

# FUNGSI MENGEDIT BUKU YANG DIPINJAM
def updatebukudipinjam(id): 
    getbuku = get_buku(id)
    kodebukuold = str(db.session.query(buku.kodebuku).filter_by(id=id).first()[0])
    judulold = str(db.session.query(buku.judul).filter_by(id=id).first()[0])
    genreold = str(db.session.query(buku.genre).filter_by(id=id).first()[0])
    lokasiold = str(db.session.query(buku.lokasi).filter_by(id=id).first()[0])
    strold = "_updated_"
    epoch = str(time.time())
    kodebukuold += strold
    kodebukuold += epoch
    if request.method == 'POST':
        kodebuku = request.form['kodebuku']
        judul = request.form['judul']
        genre = request.form['genre']
        lokasi = request.form['lokasi']
        status = request.form['status']
        flag = request.form['flag']
        created_by = request.form['created_by']
        updated_by = request.form['updated_by']
        messagebuku = ''

        if not kodebuku:
            messagebuku = 'Masukkan Kode Buku'
        elif not judul:
            messagebuku = 'Masukkan Judul Buku'
        elif not genre:
            messagebuku = 'Masukkan Genre Buku'
        elif not lokasi:
            messagebuku = 'Tulis Lokasi Rak Buku'
            
        if not messagebuku:
            updateData = buku.query.filter_by(id=id).first()
            updateData.kodebuku = kodebukuold
            updateData.judul = judulold
            updateData.genre = genreold
            updateData.lokasi = lokasiold
            updateData.updated_at = datetime.now()
            updateData.updated_by = updated_by
            updateData.flag = flag
            db.session.commit()
            insertData = buku(kodebuku=kodebuku, judul=judul, genre=genre, lokasi=lokasi, status=status, created_by=created_by)
            db.session.add(insertData)
            db.session.commit()
            flash('BERHASIL MENGEDIT DATA BUKU', category="flash-ok")
            return redirect(url_for('buku.databuku'))

        else:
            flash(messagebuku, category="flash-error")
        
    return render_template('buku/updatebukudipinjam.html', getbuku=getbuku)

# FUNGSI MENGHAPUS DATA BUKU
def deletebuku(id): 
    get_buku(id)
    epoch = str(time.time())
    delstr = "_deleted_"
    kodebuku = str(db.session.query(buku.kodebuku).filter_by(id=id).first()[0])
    kodebuku += delstr
    kodebuku += epoch
    if request.method == 'POST':
        updated_by = request.form['updated_by']
        updateData = buku.query.filter_by(id=id).first()
        updateData.kodebuku = kodebuku
        updateData.updated_at = datetime.now()
        updateData.updated_by = updated_by
        updateData.flag = "deleted"
        db.session.commit()
        flash('Berhasil Menghapus Data Buku', category="flash-ok")
        return redirect(url_for('buku.databuku'))
        db.session.close()

# FUNGSI MENDOWNLOAD / MENGKEXPORT DATA BUKU DENGAN FORMAT CSV
def downloadbuku():
    ci = cj = cg = cp = ca = ''
    bukucsv = []
    bukucsv = db.session.query(buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter_by(status='ada', flag='on').all()
    if request.method == 'POST':

        if 'downloaddatabuku' in request.form:

            carikodebuku  = ci = request.form['ci']
            carijudul = cj = request.form['cj']
            carigenre = cg = request.form['cg']
            caripinjam = cp = request.form.get('cp')
            cariada = ca = request.form.get('ca')

            if cp == 'None' and ca == 'None':
                cp = ca = ''
            elif cp == 'None' and ca == 'ada':
                cp = ''
            elif cp == 'dipinjam' and ca == 'None':
                ca = ''

            ci = cj = cg = p = "%"
            ci += str(carikodebuku)
            ci += p
            cj += str(carijudul)
            cj += p
            cg += str(carigenre)
            cg += p

            if not cp and not ca:
                bukucsv = db.session.query(buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.flag=="on").all()
            elif not cp and ca:
                bukucsv = db.session.query(buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.status==ca, buku.flag=="on").all()
            elif cp and not ca:
                bukucsv = db.session.query(buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.status==cp, buku.flag=="on").all()
            elif cp and ca:
                bukucsv = db.session.query(buku.kodebuku, buku.judul, buku.genre, buku.lokasi, buku.status).filter(buku.kodebuku.like(ci), buku.judul.like(cj), buku.genre.like(cg), buku.flag=="on").all()
    
    export_buku = ['KODE BUKU', 'JUDUL BUKU', 'GENRE', 'LOKASI', 'STATUS BUKU']
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(export_buku)
    cw.writerows(bukucsv)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=databuku.csv"
    output.headers["Content-type"] = "text/csv"
    # flash('Data Berhasil Diunduh', category="flash-ok")
    return output

# FUNGSI MENDOWNLOAD FORMAT UPLOAD BUKU MENGGUNAKAN CSV
def downloadformatbuku():
    ci = ''
    if request.method == 'POST':

        if 'downloadformatbuku' in request.form:
            carikodebuku  = ci = request.form['ci']

            ci = p = "%"
            ci += str(carikodebuku)
            ci += p

    export_buku = ['KODE BUKU', 'JUDUL BUKU', 'GENRE', 'LOKASI']
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(export_buku)
    cw.writerows(db.session.query(buku).filter(buku.kodebuku.like(ci), buku.flag=="on").all())
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=databuku.csv"
    output.headers["Content-type"] = "text/csv"
    # flash('Format Data Berhasil Diunduh', category="flash-ok")
    return output