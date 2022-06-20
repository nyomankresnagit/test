from app.member import bp_member, member_controller
from app.auth.auth_controller import login_required

@bp_member.route('/datamember', methods=['GET', 'POST'])
def datamember():
    return member_controller.datamember()

@bp_member.route('/tambahmember', methods=['GET', 'POST'])
@login_required
def tambahmember():
    return member_controller.tambahmember()

@bp_member.route('/searchmember', methods=['GET', 'POST'])
def searchmember():
    return member_controller.searchmember()

@bp_member.route('/downloadmember', methods=['GET', 'POST'])
@login_required
def downloadmember():
    return member_controller.downloadmember()

@bp_member.route('/downloadformatmember', methods=['GET', 'POST'])
@login_required
def downloadformatmember():
    return member_controller.downloadformatmember()

@bp_member.route('/uploadmember', methods=['GET', 'POST'])
@login_required
def uploadmember():
    return member_controller.uploadmember()

@bp_member.route('/updatemember/<int:id>', methods=['GET', 'POST'])
@login_required
def updatemember(id):
    return member_controller.updatemember(id)

@bp_member.route('/deletemember/<int:id>', methods=['POST'])
@login_required
def deletemember(id):
    return member_controller.deletemember(id)