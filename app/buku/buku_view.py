from app.buku import bp_buku, buku_controller
from app.auth.auth_controller import login_required

@bp_buku.route('/databuku', methods=['GET', 'POST'])
def databuku():
    return buku_controller.databuku()

@bp_buku.route('/tambahbuku', methods=['GET', 'POST'])
def tambahbuku():
    return buku_controller.tambahbuku()

@bp_buku.route('/uploadbuku', methods=['GET', 'POST'])
@login_required
def uploadbuku():
    return buku_controller.uploadbuku()

@bp_buku.route('/searchbuku', methods=['GET', 'POST'])
def searchbuku():
    return buku_controller.searchbuku()


@bp_buku.route('/updatebukuada/<int:id>', methods=['GET', 'POST'])
@login_required
def updatebukuada(id):
    return buku_controller.updatebukuada(id)

@bp_buku.route('/updatebukudipinjam/<int:id>', methods=['GET', 'POST'])
@login_required
def updatebukudipinjam(id): 
    return buku_controller.updatebukudipinjam(id)

@bp_buku.route('/deletebuku/<int:id>', methods=['POST'])
@login_required
def deletebuku(id):
    return buku_controller.deletebuku(id)

@bp_buku.route('/downloadbuku', methods=['GET', 'POST'])
@login_required
def downloadbuku():
    return buku_controller.downloadbuku()

@bp_buku.route('/downloadformatbuku', methods=['GET', 'POST'])
@login_required
def downloadformatbuku():
    return buku_controller.downloadformatbuku()