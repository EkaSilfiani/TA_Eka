from flask_wtf import Form
from wtforms import FileField, SubmitField
from datetime import datetime
import pymysql
import config

class MSimpanUser:
	def __init__ (self,no=None, level=None, nama=None, username=None, password=None, tanggal_lahir=None, jenis_kelamin=None, no_telp=None, alamat=None):
		self.no = no
		self.level = level
		self.nama = nama
		self.username = username
		self.password = password
		self.tanggal_lahir = tanggal_lahir
		self.jenis_kelamin = jenis_kelamin
		self.no_telp = no_telp
		self.alamat = alamat

	def openDB (self):
		global db, cursor
		db = pymysql.connect(
			config.DB_HOST,
			config.DB_USER,
			config.DB_PASSWORD,
			config.DB_NAME)
		cursor = db.cursor()

	def closeDB(self):
		global db, cursor
		db.close()

	def selectDB(self):
		self.openDB()
		cursor.execute("SELECT * FROM user")
		container = []
		self.closeDB()
		return container

	def insertDB(self, data):
		self.openDB()
		cursor.execute("INSERT INTO user (username, password, nama, level, tanggal_lahir, jenis_kelamin, no_telp, alamat) VALUES( '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s')" % data)
		db.commit()
		self.closeDB()