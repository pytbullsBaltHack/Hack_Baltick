
import sqlite3
import numpy

class Database(object):
    conn = False
    
    def __init__(self,filename):
        self.conn = sqlite3.connect(filename)
    
        return

    def query(self,q):
        cursor = self.conn.cursor()
        cursor.execute(q)
        self.conn.commit()
        return  cursor.lastrowid
        
    def querySingle(self,q):
        cursor = self.conn.cursor()
        cursor.execute(q)
        results = cursor.fetchone()
        return results
        
    def queryAll(self,q):
        cursor = self.conn.cursor()
        cursor.execute(q)
        results = cursor.fetchall()
        return results
       
    # Получить список известных и обработанных пользователей
    def GetUserList(self):
        q = "SELECT id as id, face_id as face_id, name as name FROM webface_userface"
    
        print(q)
        return []
        
    # Отправить задетектенного пользователя
    def PushUserId(self,userid):
        q = "INSERT INTO webface_userface (face_id,img,name) VALUES('{0}','','')".format(userid.tostring())
        #self.query(q)
        
        return
    
    # Отправить задетектенного пользователя
    def PushVisitor(self,userid,id,event):
        q = "INSERT INTO webface_visitor (face_id,date,user_id,event) VALUES('{0}',DATETIME('now'),{1},{2})".format(userid.tostring(),id,event)
        self.query(q)
        
        print(q)
        
        return
    