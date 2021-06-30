import pymysql
import config

db = cursor = None

class Survei():
    def __init__ (self, username=None, password=None):
        self.username = username
        self.password = password

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

    def authenticate(self):
        self.openDB()
        cursor.execute("SELECT COUNT(*) FROM user WHERE username = '%s' And password = '%s'" % (self.username, self.password))
        count_account = (cursor.fetchone())[0]
        self.closeDB()
        return True if count_account > 0 else False

    def accountType(self):
        self.openDB()
        cursor.execute("SELECT * FROM user WHERE username = '%s' AND password = '%s'" % (self.username, self.password))
        account = (cursor.fetchone())
        self.closeDB()
        if account[1] =='faskes':
            return 'faskes'
        elif account[1] == 'kelurahan':
            return 'kelurahan'
        elif account[1] == 'jumantik':
            return 'jumantik'