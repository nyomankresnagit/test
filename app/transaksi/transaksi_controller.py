from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for, make_response
)
import os
from os.path import join, dirname, realpath
from werkzeug.exceptions import abort
import time
from datetime import datetime, timedelta
from io import StringIO
import csv
from app import db
from app.auths.auth_model import admin
from app.buku.buku_model import buku
from app.member.member_model import member
from app.transaksi.transaksi_model import transaksi

################################ CEKLIS ##########################
# Tambah Transaksi = CLEAR
# Display Transaksi = CLEAR
# Search Transaksi = CLEAR
# Download Transaksi = CLEAR
# Pengembalian Transaksi = CLEAR

def index():
    transaksis = searchtransaksi()[0]
    cp = searchtransaksi()[1]
    cj = searchtransaksi()[2]
    cw1 = searchtransaksi()[3]
    cw2 = searchtransaksi()[4]
    return render_template('transaksi/index.html', transaksis=transaksis, cp=cp, cj=cj, cw1=cw1, cw2=cw2)

def searchtransaksi():
    cp = cj = cw1 = cw2 = ''
    transaksisearch = []
    transaksisearch = db.session.query(transaksi).join(buku).join(member).join(admin).filter(transaksi.flag == "on").with_entities(transaksi.id, member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin.nama, transaksi.flag).all()
    
    if request.method == 'POST': #search data berdasarkan input = 4 jenis, Logika Searching 2^input = 16
        if 'caridatatransaksi' in request.form:
            caripeminjam = cp = request.form['caripeminjam']
            carijudul = cj = request.form['carijudul']
            cariwaktu1 = cw1 = request.form['cariwaktu1']
            cariwaktu2 = cw2 = request.form['cariwaktu2']

            if not cw1 and not cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksisearch = db.session.query(transaksi).join(buku).join(member).join(admin).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.flag == "on").with_entities(transaksi.id, member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin.nama, transaksi.flag).all()
            elif not cw1 and cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksisearch = db.session.query(transaksi).join(buku).join(member).join(admin).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.tgl_kembali <= cw2, transaksi.flag == "on").with_entities(transaksi.id, member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin.nama, transaksi.flag).all()
            elif cw1 and not cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksisearch = db.session.query(transaksi).join(buku).join(member).join(admin).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.tgl_kembali >= cw1, transaksi.flag == "on").with_entities(transaksi.id, member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin.nama, transaksi.flag).all()
            elif cw1 and cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksisearch = db.session.query(transaksi).join(buku).join(member).join(admin).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.tgl_kembali.between(cw1, cw2), transaksi.flag == "on").with_entities(transaksi.id, member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin.nama, transaksi.flag).all()
                
    return transaksisearch, cp, cj, cw1, cw2

#############################################################################
def tambahtransaksi():
    if request.method == 'POST':
        idmember = request.form['idmember']
        kodebuku = request.form['kodebuku']
        jumlah_hari = request.form['jumlah_hari']
        idadmin = request.form['idadmin']
        created_by = request.form['created_by']
        datamember = db.session.query(member.idmember).filter_by(idmember=idmember).first()
        databuku = db.session.query(buku.judul).filter_by(kodebuku=kodebuku).first()
        datapinjam = db.session.query(buku.kodebuku).filter_by(kodebuku=kodebuku, status='ada').first()
        messagetransaksi = ''
        for i in databuku:
            judulbuku = i
        if not idmember:
            messagetransaksi = 'masukkan id member'
        elif not kodebuku:
            messagetransaksi = 'masukkan kode buku'
        elif not jumlah_hari:
            messagetransaksi = 'masukkan tanggal pengembalian'
        elif not databuku and not datamember:
            messagetransaksi = 'Data member dan buku tidak ditemukan'
        elif not datamember:
            messagetransaksi = 'Data member tidak ditemukan'
        elif databuku and not datapinjam:
            messagetransaksi = 'Buku ' + str(judulbuku) + ' sedang dipinjam'
        elif not databuku:
            messagetransaksi = 'Data buku tidak ditemukan'
        
        if not messagetransaksi:
            tgl_kembali = datetime.now().date() + timedelta(days=int(jumlah_hari))
            insertData = transaksi(idmember=idmember, kodebuku=kodebuku, tgl_kembali=tgl_kembali, idadmin=idadmin, created_by=created_by)
            db.session.add(insertData)
            db.session.commit()
            updateData = buku.query.filter_by(kodebuku=kodebuku).first()
            updateData.status = "dipinjam"
            db.session.commit()
            flash('Berhasil Menambah Transaksi', category="flash-ok")
            return redirect(url_for('index'))
            db.session.close()

    flash(messagetransaksi, category="flash-error")
    return redirect(url_for('index'))

def get_transaksi(id):
    gettransaksi = transaksi.query.filter_by(id=id).first()

    if not gettransaksi:
        abort(404, f"transaksi dengan id {id} tidak ditemukan")

    return gettransaksi


def updatetransaksi(id):
    gettransaksi = get_transaksi(id)
    if request.method == 'POST':
        idmember = request.form['idmember']
        kodebuku = request.form['kodebuku']
        tgl_kembali = request.form['tgl_kembali']
        flag = request.form['flag']
        updated_by = request.form['updated_by']
        messagetransaksi = ''

        if not kodebuku:
            messagetransaksi = 'masukkan kode kodebuku'
        elif not idmember:
            messagetransaksi = 'masukkan id member'
        elif not tgl_kembali:
            messagetransaksi = 'masukkan tanggal kembali'

        if not messagetransaksi:
            updateDataBuku = buku.query.filter_by(kodebuku=kodebuku).first()
            updateDataBuku.status = "ada"
            db.session.commit()
            updateDataTransaksi = transaksi.query.filter_by(id=id).first()
            updateDataTransaksi.updated_at = datetime.now()
            updateDataTransaksi.updated_by = updated_by
            updateDataTransaksi.flag = flag
            db.session.commit()
            flash('Buku Berhasil Dikembalikan', category="flash-ok")
            return redirect(url_for('index'))
            db.session.close()

        else:
            flash(messagetransaksi, category="flash-error")
        
    return render_template('transaksi/updatetransaksi.html', gettransaksi=gettransaksi)

def downloadtransaksi():
    cp = cj = cw1 = cw2 = ''
    transaksicsv = []
    transaksicsv = db.session.query(transaksi).join(buku).join(member).join(admin).filter(transaksi.flag == "on").with_entities(member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin.nama).all()
    
    if request.method == 'POST': #search data 
        if 'downloaddatatransaksi' in request.form:
            caripeminjam = cp = request.form['cp']
            carijudul = cj = request.form['cj']
            cariwaktu1 = cw1 = request.form['cw1']
            cariwaktu2 = cw2 = request.form['cw2']
            if cw1 == 'None':
                cw1 = ''
            elif cw2 == 'None':
                cw2 = ''

            if not cw1 and not cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksicsv = db.session.query(transaksi).join(buku).join(member).join(admin).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.flag == "on").with_entities(member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin.nama).all()
            elif not cw1 and cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksicsv = db.session.query(transaksi).join(buku).join(member).join(admin).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.tgl_kembali <= cw2, transaksi.flag == "on").with_entities(member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin.nama).all()
            elif cw1 and not cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksicsv = db.session.query(transaksi).join(buku).join(member).join(admin).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.tgl_kembali >= cw1, transaksi.flag == "on").with_entities(member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin.nama).all()
            elif cw1 and cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksicsv = db.session.query(transaksi).join(buku).join(member).join(admin).filter(member.nama.like(cp), buku.judul.like(cj), transaksi.tgl_kembali.between(cw1, cw2), transaksi.flag == "on").with_entities(member.nama, buku.judul, transaksi.tgl_pinjam, transaksi.tgl_kembali, admin.nama).all()

    export_transaksi = ['NAMA PEMINJAM', 'JUDUL BUKU', 'TANGGAL PINJAM', 'TANGGAL KEMBALI', 'NAMA ADMIN']
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(export_transaksi)
    cw.writerows(transaksicsv)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=datatransaksi.csv"
    output.headers["Content-type"] = "text/csv"
    # flash('Data Berhasil Diunduh')
    return output