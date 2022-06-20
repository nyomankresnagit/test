from app.transaksi import bp_transaksi, transaksi_controller
from app.auth.auth_controller import login_required
from flask import render_template



@bp_transaksi.route('/datatransaksi', methods=['GET', 'POST'])
def index():
    return transaksi_controller.index()



@bp_transaksi.route('/downloadtransaksi', methods=('GET','POST'))
@login_required
def downloadtransaksi():
    return transaksi_controller.downloadtransaksi()

@bp_transaksi.route('/tambahtransaksi', methods=('GET', 'POST'))
@login_required
def tambahtransaksi():
    return transaksi_controller.tambahtransaksi()

@bp_transaksi.route('/updatetransaksi/<int:id>', methods=('GET', 'POST'))
@login_required
def updatetransaksi(id):
    return transaksi_controller.updatetransaksi(id)