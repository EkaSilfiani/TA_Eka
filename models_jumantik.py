import pymysql
import config

db = cursor = None

class MJumantik:
	def __init__ (self, id_jumantik=None, kode_desa=None, nama=None, alamat=None, no_telp=None, jenis_kelamin=None, 
		area_kerja=None):
		self.id_jumantik = id_jumantik
		self.kode_desa = kode_desa
		self.nama = nama
		self.alamat= alamat
		self.no_telp = no_telp
		self.jenis_kelamin = jenis_kelamin
		self.area_kerja = area_kerja

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
		cursor.execute("SELECT * FROM jumantik")
		container = []
		for id_jumantik, kode_desa, nama, alamat, no_telp, jenis_kelamin, area_kerja in cursor.fetchall():
			container.append((id_jumantik, kode_desa, nama, alamat, no_telp, jenis_kelamin, area_kerja))
		self.closeDB()
		return container

	def insertDB(self, data):
		self.openDB()
		cursor.execute("INSERT INTO jumantik (id_jumantik, kode_desa, nama, alamat, no_telp, jenis_kelamin, area_kerja) VALUES('%s','%s','%s','%s','%s','%s','%s')" % data)
		db.commit()
		self.closeDB()
		
	def get_jumantikDBbyNo(self, id_jumantik):
		self.openDB()
		cursor.execute("SELECT * FROM jumantik WHERE id_jumantik='%s'" % id_jumantik)
		data = cursor.fetchone()
		return data

	def update_jumantikDB(self, data):
		self.openDB()
		cursor.execute("UPDATE jumantik SET kode_desa='%s', nama='%s', alamat='%s', no_telp='%s', jenis_kelamin='%s', area_kerja='%s' WHERE id_jumantik=%s" % data)
		db.commit()
		self.closeDB()

	def deleteDB(self, id_jumantik):
		self.openDB()
		cursor.execute("DELETE FROM jumantik WHERE id_jumantik=%s" % id_jumantik)
		db.commit()
		self.closeDB()