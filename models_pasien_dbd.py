import pymysql
import config

db = cursor = None

class MPasien_Dbd:
	def __init__ (self, no=None, tanggal_masuk=None, no_ktp=None, nama_pasien=None, alamat=None, 
		tempat_tanggal_lahir=None, jenis_kelamin=None, pekerjaan=None):
		self.no = no
		self.tanggal_masuk = tanggal_masuk
		self.no_ktp= no_ktp
		self.nama_pasien = nama_pasien
		self.alamat = alamat
		self.tempat_tanggal_lahir = tempat_tanggal_lahir
		self.jenis_kelamin = jenis_kelamin
		self.pekerjaan = pekerjaan

	def openDB(self):
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
		cursor.execute("SELECT * FROM pasien_dbd")
		container = []
		for no, tanggal_masuk, no_ktp, nama_pasien,alamat,tempat_tanggal_lahir, jenis_kelamin, pekerjaan in cursor.fetchall():
			container.append((no, tanggal_masuk, no_ktp, nama_pasien,alamat,tempat_tanggal_lahir, jenis_kelamin, pekerjaan))
		self.closeDB()
		return container

	def insertDB(self, data):
		self.openDB()
		cursor.execute("INSERT INTO pasien_dbd (tanggal_masuk, no_ktp, nama_pasien, alamat, tempat_tanggal_lahir, jenis_kelamin, pekerjaan) VALUES('%s','%s','%s','%s','%s','%s','%s')" % data)
		db.commit()
		self.closeDB()
		
	def getDBbyNo(self, no):
		self.openDB()
		cursor.execute("SELECT * FROM pasien_dbd WHERE no='%s'" % no)
		data = cursor.fetchone()
		return data

	def updateDB(self, data):
		self.openDB()
		cursor.execute("UPDATE pasien_dbd SET tanggal_masuk='%s', no_ktp='%s', nama_pasien='%s', alamat='%s', tempat_tanggal_lahir='%s', jenis_kelamin='%s', pekerjaan='%s' WHERE no=%s" % data)
		db.commit()
		self.closeDB()

	def deleteDB(self, no):
		self.openDB()
		cursor.execute("DELETE FROM pasien_dbd WHERE no=%s" % no)
		db.commit()
		self.closeDB()