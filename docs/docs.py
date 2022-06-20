from flask import *

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/dokter')
def dokter():
    return render_template("dokter.html")

@app.route('/dokterHistory')
def dokterHistory():
    return render_template("dokter_history.html")

@app.route('/pasien')
def pasien():
    return render_template("pasien.html")

@app.route('/pasienHistory')
def pasienHistory():
    return render_template("pasien_history.html")

@app.route('/trans')
def trans():
    return render_template("trans.html")