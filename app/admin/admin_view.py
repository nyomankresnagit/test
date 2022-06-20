from app.admin import admin_bp, admin_controller, admin_model

@admin_bp.route('/viewAdmin')
def viewAdmin():
    return admin_controller.viewAdmin()

@admin_bp.route('/addAdmin', methods=['POST'])
def addAdmin():
    return admin_controller.addAdmin()

@admin_bp.route('/deleteAdmin/<string:idAdmin>')
def deleteAdmin(idAdmin):
    return admin_controller.deleteAdmin(idAdmin)

@admin_bp.route('/editAdmin/<string:idAdmin>')
def editAdmin(idAdmin):
    return admin_controller.editAdmin(idAdmin)

@admin_bp.route('/searchAdmin', methods=['POST'])
def searchAdmin():
    return admin_controller.searchAdmin()