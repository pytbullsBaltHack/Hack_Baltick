
import sqlite3

class Database(object):
    conn = False
    
    def __init__(self,filename):
        self.conn = sqlite3.connect(filename)
    
        return

    def query(self,q):
        cursor = self.conn.cursor()
        cursor.execute(q)
        conn.close()
        return
        
    def querySingle(self,q):
        cursor = self.conn.cursor()
        cursor.execute(q)
        results = cursor.fetchone()
        conn.close()
        return results
        
    def queryAll(self,q):
        cursor = self.conn.cursor()
        cursor.execute(q)
        results = cursor.fetchall()
        conn.close()
        return results
       
    # Получить список известных и обработанных пользователей
    def GetUserList(self):
        return []
        
    # Отправить задетектенного пользователя
    def PushUserId(self,userid,id):
        return
    
    