from app.admin_history import admin_history_bp, admin_history_controller, admin_history_model

@admin_history_bp.route('/viewAdminHistory')
def viewAdminHistory():
    return admin_history_controller.viewAdminHistory()

@admin_history_bp.route('/addAdminHistory')
def addAdminHistory():
    return admin_history_controller.addAdminHistory()