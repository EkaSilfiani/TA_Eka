import pymysql
import config

db=cursor=None

class UploadFile:
	def __init__(self, id_file=None, id_jumantik=None, nama_file=None, tgl_file=None):
		self.id_file=id_file
		self.id_jumantik = id_jumantik
		self.nama_file= nama_file
		self.tgl_file=tgl_file

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
		cursor.execute("SELECT * FROM uploadfile")
		container = []
		for id_file,id_jumantik, nama_file,tgl_file in cursor.fetchall():
			container.append((id_file,id_jumantik, nama_file,tgl_file))
		self.closeDB()
		return container

	def insertDB(self, data):
		self.openDB()
		cursor.execute("INSERT INTO uploadfile (id_jumantik, nama_file, tgl_file) VALUES ('%s','%s', '%s')" % data)
		db.commit()
		self.closeDB()

	def getDBbyNo(self, id_file):
		self.openDB()
		cursor.execute("SELECT * FROM uploadfile WHERE id_file='%s'" % id_file)
		data = cursor.fetchone()
		return data