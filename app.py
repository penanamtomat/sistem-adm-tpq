from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
# import pymongo
# from pymongo import MongoClient

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TPQ Al-Baidhowi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#objek koneksi
# client = MongoClient("mongodb://localhost:27017/")

#using database
# db = client['tpqbaidhowi']

#menggunakan koleksi
# collection = db['pendaftaran']

# instance sqlalchemy
db = SQLAlchemy(app)

# #instance migrate
migrate = Migrate(app, db)

#membuat variabel untuk menyimpan file
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Pendaftaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    ttl = db.Column(db.String(50))
    ayah = db.Column(db.String(50))
    job_ayah = db.Column(db.String(50))
    ibu = db.Column(db.String(50))
    job_ibu = db.Column(db.String(50))
    jenis_kelamin = db.Column(db.String(50))
    jadwal = db.Column(db.String(50))
    no_hp = db.Column(db.String(50))
    alamat = db.Column(db.String(200))
    tahunan = db.Column(db.String(50))
    spp = db.Column(db.String(50))
    kartu_keluarga = db.Column(db.String(50))

    def __repr__(self):
        return '<Pendaftaran %r>' % self.nama

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def landing_page():
    return render_template('landingpage.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/antrian")
def antri():
    list_santri = Pendaftaran.query.all() 
    return render_template('antrian.html', santri = list_santri)

@app.route("/pendaftaran")
def daftar():
    return render_template('pendaftaran.html')

@app.route("/pendaftaran/save", methods=['POST'])
def pendaftaran_save():
    # print(request.form.get('name'))
    # print(request.form.get('ttl'))
    # print(request.form.get('dadname'))
    # print(request.form.get('dadkerja'))
    # print(request.form.get('momname'))
    # print(request.form.get('momkerja'))

    #menerima data dari request
    receive_nama = request.form.get('name')
    receive_ttl = request.form.get('ttl')
    receive_dadname = request.form.get('dadname')
    receive_dadkerja = request.form.get('dadkerja')
    receive_momname = request.form.get('momname')
    receive_momkerja = request.form.get('momkerja')
    receive_jenis_kelamin = request.form.get('jeniskelamin')
    receive_jadwal = request.form.get('jadwal')
    receive_no_hp = request.form.get('nohp')
    receive_alamat = request.form.get('alamat')
    receive_tahunan = request.form.get('tahunan')
    receive_spp = request.form.get('spp')
    receive_file = request.files['kartukeluarga']

    if receive_file and allowed_file(receive_file.filename):
            filename = secure_filename(receive_file.filename)
            receive_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #instance / mencetak --> database
            santri = Pendaftaran()
            santri.nama = receive_nama
            santri.ttl = receive_ttl
            santri.ayah = receive_dadname
            santri.job_ayah = receive_dadkerja
            santri.ibu = receive_momname
            santri.job_ibu = receive_momkerja
            santri.jenis_kelamin = receive_jenis_kelamin
            santri.jadwal = receive_jadwal
            santri.no_hp = receive_no_hp
            santri.alamat = receive_alamat
            santri.tahunan = receive_tahunan
            santri.spp = receive_spp
            santri.kartu_keluarga = 'uploads/' + filename

            db.session.add(santri)
            db.session.commit()

            return redirect('/pendaftaran')

#update data
@app.route('/<id>/update')
def update_status(id):
    santri = Pendaftaran.query.filter_by(id=id).first()
    return render_template('update-status.html', santri = santri)

@app.route('/<id>/update/save', methods=['POST'])
def save_update(id):
    update_nama = request.form.get('name')
    update_ttl = request.form.get('ttl')
    update_dadname = request.form.get('dadname')
    update_dadkerja = request.form.get('dadkerja')
    update_momname = request.form.get('momname')
    update_momkerja = request.form.get('momkerja')
    update_jenis_kelamin = request.form.get('jeniskelamin')
    update_jadwal = request.form.get('jadwal')
    update_no_hp = request.form.get('nohp')
    update_alamat = request.form.get('alamat')
    update_tahunan = request.form.get('tahunan')
    update_spp = request.form.get('spp')
    update_kartu_keluarga = request.files['kartukeluarga']

    santri = Pendaftaran.query.filter_by(id=id).first()

    #mengubah data yang diambil dari database
    santri.nama = update_nama
    santri.ttl = update_ttl
    santri.ayah = update_dadname
    santri.job_ayah = update_dadkerja
    santri.ibu = update_momname
    santri.job_ibu = update_momkerja
    santri.jenis_kelamin = update_jenis_kelamin
    santri.jadwal = update_jadwal
    santri.no_hp = update_no_hp
    santri.alamat = update_alamat
    santri.tahunan = update_tahunan
    santri.spp = update_spp
    santri.kartu_keluarga = 'uploads/' + update_kartu_keluarga.filename

    db.session.add(santri)
    db.session.commit()

    return redirect('/antrian')

@app.route('/<id>/delete')
def hapus_santri(id):
    santri = Pendaftaran.query.filter_by(id=id).first()
    db.session.delete(santri)
    db.session.commit()

    return redirect('/antrian')

if __name__ == "__main__":
    app.run(debug=True, port=5002)