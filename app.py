from flask import Flask, render_template, jsonify, json, session, \
request, redirect, url_for
from models import Survei
from models_pasien_dbd import MPasien_Dbd
from models_data_survei import MData_Survei
from models_jumantik import MJumantik
from models_uploadfile import UploadFile
from models_buat_akun import MSimpanUser
from werkzeug import secure_filename
from datetime import datetime
import pymysql
import time
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = '1234567890!@#$%^&*()'
application.config['UPLOAD_FOLDER'] = os.path.realpath('.') + \
	'/Fasilitas kesehatan 1.6 memel/static/uploads'
#Satuan Byte
application.config['MAX_CONTENT_PATH'] = 10000000

@application.route('/')
def index():
	if 'username' in session and session['level'] == 'faskes':
		username = session['username']
		level = session['level']
		return render_template('index_faskes.html', username = username, level=level)
	elif 'username' in session and session['level'] == 'kelurahan':
		username = session['username']
		level = session['level']
		return render_template('index_kelurahan.html', username = username, level=level)
	elif 'username' in session and session['level'] == 'jumantik':
		username = session['username']
		level = session['level']
		return render_template('index_jumantik.html', username = username, level=level)
	return redirect(url_for('login'))

@application.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pengguna = Survei(username, password)
        if pengguna.authenticate():
            session['username'] = username
            session['level'] = pengguna.accountType()
            return redirect(url_for('index'))
        msg = 'Salah!'
        return render_template('login.html', msg = msg)
    return render_template('login.html')

@application.route('/logout')
def logout():
    session.pop('username', '')
    return redirect(url_for('index'))
#<--------------------------------------HOME FASKES--------------------------------------->
@application.route('/home_faskes')
def home_faskes():
    return render_template("index_faskes.html")
 #<--------------------------------------HOME KELURAHAN----------------------------------->
@application.route('/home_kelurahan')
def home_kelurahan():
    return render_template("index_kelurahan.html")
 #<--------------------------------------HOME JUMANTIK------------------------------------>
@application.route('/home_jumantik')
def home_jumantik():
    return render_template("index_jumantik.html")
#<------------------------------------------FORM PASIEN DBD-------------------------------------->
@application.route('/datapasien')
def datapasien():
	models = MPasien_Dbd()
	container = []
	container = models.selectDB()
	return render_template('pasien_dbd.html',container=container)

@application.route('/insert_data_pasien', methods=['GET', 'POST'])
def insert_data_pasien():
	if request.method == 'POST':
		tanggal_masuk = request.form['tanggal_masuk']
		no_ktp = request.form['no_ktp']
		nama_pasien = request.form['nama_pasien']
		alamat = request.form['alamat']
		tempat_tanggal_lahir = request.form['tempat_tanggal_lahir']
		jenis_kelamin = request.form['jenis_kelamin']
		pekerjaan = request.form['pekerjaan']
		data = (tanggal_masuk, no_ktp, nama_pasien, alamat, tempat_tanggal_lahir, jenis_kelamin, pekerjaan)
		models = MPasien_Dbd()
		models.insertDB(data)
		return redirect(url_for('datapasien'))
	else:
		return render_template('insert_form_pasien.html')

@application.route('/update/<no>')
def update(no):
	models = MPasien_Dbd()
	data = models.getDBbyNo(no)
	return render_template('update_form_pasien.html', data= data)

@application.route('/update_prosess', methods=['GET', 'POST'])
def update_prosess():
	no = request.form['no']
	tanggal_masuk = request.form['tanggal_masuk']
	no_ktp = request.form['no_ktp']
	nama_pasien = request.form['nama_pasien']
	alamat = request.form['alamat']
	tempat_tanggal_lahir = request.form['tempat_tanggal_lahir']
	jenis_kelamin = request.form['jenis_kelamin']
	pekerjaan = request.form['pekerjaan']
	data = (tanggal_masuk, no_ktp, nama_pasien, alamat, tempat_tanggal_lahir, jenis_kelamin, pekerjaan, no)
	models = MPasien_Dbd()
	models.updateDB(data)
	return redirect(url_for('datapasien'))

@application.route('/delete/<no>')
def delete(no):
	models = MPasien_Dbd()
	models.deleteDB(no)
	return redirect(url_for('datapasien'))

#------------------------------------------------ DATA SURVEI FASKES ---------------------->
@application.route('/datasurveifaskes')
def datasurveifaskes():
	models = MData_Survei()
	container = []
	container = models.selectDB()
	return render_template('form_survei_jumantik.html',container=container)

#------------------------------------------------ DATA SURVEI KELURAHAN ---------------------->
@application.route('/datasurveikelurahan')
def datasurveikelurahan():
	models = MData_Survei()
	container = []
	container = models.selectDB()
	return render_template('form_survei_jumantik1.html',container=container)

#------------------------------------------------ DATA SURVEI JUMANTIK ---------------------->
@application.route('/datasurveijumantik')
def datasurveijumantik():
	models = MData_Survei()
	container = []
	container = models.selectDB()
	return render_template('form_survei.html',container=container)
#<------------------------------------- FORM SURVEI JUMANTIK ---------------------->
@application.route('/data_survei_jumantik')
def data_survei_jumantik():
	models = MData_Survei()
	container = []
	container = models.selectDB()
	return render_template('form_survei_jumantik2.html', container=container)

@application.route('/insert_data_survei_jumantik', methods=['GET', 'POST'])
def insert_data_survei_jumantik():
	if request.method == 'POST':
		tanggal_survei = request.form['tanggal_survei']
		id_jumantik = request.form['id_jumantik']
		no_kk = request.form['no_kk']
		nama_kepala_keluarga = request.form['nama_kepala_keluarga']
		no_telp = request.form['no_telp']
		alamat = request.form['alamat']
		bak_mandi = request.form['bak_mandi']
		drum = request.form['drum']
		kaleng_bekas = request.form['kaleng_bekas']
		tempayan = request.form['tempayan']
		lain_lain = request.form['lain_lain']
		status = request.form['status']
		jumlah_tpa = request.form ['jumlah_tpa']
		data = (tanggal_survei, id_jumantik, no_kk, nama_kepala_keluarga, no_telp, alamat,bak_mandi, drum, kaleng_bekas, tempayan, lain_lain, status, jumlah_tpa)
		models = MData_Survei()
		models.insertDB(data)
		return redirect(url_for('datasurveijumantik'))
	else:
		return render_template('insert_form_survei_jumantik.html')

@application.route('/update_form_survei/<no>')
def update_form_survei(no):
	models = MData_Survei()
	data = models.get_surveiDBbyNo(no)
	return render_template('update_form_survei_jumantik.html', data= data)

@application.route('/update_prosess_survei', methods=['GET', 'POST'])
def update_prosess_survei():
	no = request.form['no']
	tanggal_survei = request.form['tanggal_survei']
	id_jumantik = request.form['id_jumantik']
	no_kk = request.form['no_kk']
	nama_kepala_keluarga = request.form['nama_kepala_keluarga']
	no_telp = request.form['no_telp']
	alamat = request.form['alamat']
	bak_mandi = request.form['bak_mandi']
	drum = request.form['drum']
	kaleng_bekas = request.form['kaleng_bekas']
	tempayan = request.form['tempayan']
	lain_lain = request.form['lain_lain']
	status = request.form['status']
	jumlah_tpa = request.form ['jumlah_tpa']
	data = (tanggal_survei, id_jumantik, no_kk, nama_kepala_keluarga, no_telp, alamat,bak_mandi, drum, kaleng_bekas, tempayan, lain_lain, status, jumlah_tpa, no)
	models = MData_Survei()
	models.update_surveiDB(data)
	return redirect(url_for('data_survei_jumantik'))

@application.route('/delete_survei/<no>')
def delete_survei(no):
	models = MData_Survei()
	models.deleteDB(no)
	return redirect(url_for('data_survei_jumantik'))

#<--------------------------------DATA FILE SURVEI JUMANTIK-------------------------------->
@application.route('/file_sukses')
def file_sukses():
	models = UploadFile()
	container = []
	container = models.selectDB()
	return render_template('file_sukses.html', container=container)

@application.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		id_jumantik= request.form['id_jumantik']
		f = request.files['file']
		filename = application.config['UPLOAD_FOLDER'] + \
			 '/' + secure_filename(f.filename)
		date_time=datetime.now()
		data = (id_jumantik, secure_filename(f.filename), date_time)
		models = UploadFile()
		models.insertDB(data)
		container = []
		container = models.selectDB()
		try:
			f.save(filename)
			return render_template('file_sukses.html', container=container,
				filename=secure_filename(f.filename))
		except:
			return render_template('file_gagal.html')
	
	return render_template('form_file.html')
#<------------------------------------FORM DATA JUMANTIK----------------------------------->
@application.route('/datajumantik')
def datajumantik():
	models = MJumantik()
	container = []
	container = models.selectDB()
	return render_template('jumantik.html',container=container)

@application.route('/insert_data_jumantik', methods=['GET', 'POST'])
def insert_data_jumantik():
	if request.method == 'POST':
		id_jumantik = request.form['id_jumantik']
		kode_desa = request.form['kode_desa']
		nama = request.form['nama']
		alamat = request.form['alamat']
		no_telp = request.form['no_telp']
		jenis_kelamin = request.form['jenis_kelamin']
		area_kerja = request.form['area_kerja']
		data = (id_jumantik, kode_desa, nama, alamat, no_telp, jenis_kelamin, area_kerja)
		models = MJumantik()
		models.insertDB(data)
		return redirect(url_for('datajumantik'))
	else:
		return render_template('insert_form_jumantik.html')

@application.route('/update_jumantik/<id_jumantik>')
def update_jumantik(id_jumantik):
	models = MJumantik()
	data = models.get_jumantikDBbyNo(id_jumantik)
	return render_template('update_form_jumantik.html', data=data)

@application.route('/update_prosess_jumantik', methods=['GET', 'POST'])
def update_prosess_jumantik():
	id_jumantik = request.form['id_jumantik']
	kode_desa = request.form['kode_desa']
	nama = request.form['nama']
	alamat = request.form['alamat']
	no_telp = request.form['no_telp']
	jenis_kelamin = request.form['jenis_kelamin']
	area_kerja = request.form['area_kerja']
	data = (kode_desa, nama, alamat, no_telp, jenis_kelamin, area_kerja, id_jumantik)
	models = MJumantik()
	models.update_jumantikDB(data)
	return redirect(url_for('datajumantik'))

@application.route('/delete_jumantik/<id_jumantik>')
def delete_jumantik(id_jumantik):
	models = MJumantik()
	models.deleteDB(id_jumantik)
	return redirect(url_for('datajumantik'))

#<------------------------------------BUAT AKUN----------------------------------->
@application.route('/buat_akun', methods = ['GET', 'POST'])
def buat_akun():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nama = request.form['nama']
        level = request.form['level']
        tanggal_lahir = request.form['tanggal_lahir']
        jenis_kelamin = request.form['jenis_kelamin']
        no_telp = request.form['no_telp']
        alamat = request.form['alamat']
        data = (username, password, nama, level, tanggal_lahir, jenis_kelamin, no_telp, alamat)
        models = MSimpanUser()
        models.insertDB(data)
        return redirect(url_for('login'))
    else:
        return render_template('buat_akun.html')
#<------------------------------------------------SEARCH------------------------------------------->

if __name__ == '__main__':
	application.run(debug=True)