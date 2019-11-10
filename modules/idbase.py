import cv2
import numpy
import math
import torch

from modules.database import Database
from modules.detector_id.DetectoID import DetectorId, FaceId

class UserRecord(object):
    id = 0
    face_id = ''
    name = ''
    
    def parse(self,dbitem):
        self.id = int(dbitem[0])
        
        fid = numpy.array(eval('[' + dbitem[1] + ']'))
        tensor = torch.from_numpy(fid)
        self.face_id = FaceId(tensor)
        self.name = dbitem[2]
        
        print(self.face_id)
        return
        
    def __init__(self):
        return
        
class FaceIdBase(object):
    # список id
    idlist = []
    
    # список известных посетителей
    visitors = []
    
    # База данных
    database = False
    
    # лимит расстояния для похожести
    # TODO: брать из конфига
    similardist = 0.07
    
    # TODO: для оптимизации обеспечивать кластеризацию, 
    # т.е. при поиске сохранять результаты о похожести
    # чтобы не искать через кучу дублирующихся объектов
    
    # TODO: обеспечить выгрузку в базу старых лиц
    
    def __init__(self):
        self.idlist = []
        self.visitors = []
        self.database = Database("server/db.sqlite3")
        self.similardist = 0.07
        self.loadusers()
        return 
   
    def loadusers(self):
        users = self.database.GetUserList()
        #print(users)
        for u in users:
            ur = UserRecord()
            ur.parse(u)
            self.visitors.append(ur)
            print('added user {0}\n'.format(ur.name))
            print(ur.face_id)
        return
    def detectuser(self,id):
        mindist = self.similardist
        minuser = None
        for v in self.visitors:
            dist = id.calcDistance(v.face_id)
            #print(id.id)
            #print(v.face_id.id)
           # print("Dist: {0} to {1}".format(dist,v.id))
            if (dist < mindist):
                mindist = dist
                minuser = v
                
        return minuser
        
    def addnewuser(self,nid,id):
        ur = UserRecord()
        ur.id = nid
        ur.face_id = id
        ur.name = 'unk {0}'.format(nid)
        self.visitors.append(ur)
        return
    
    # Попробуем найти похожие id в базе, возвращаем индексы похожих
    def getSimilarObjects(self,id):
        ret = []
        
        for i in range(0, len(self.idlist)):
            oid = self.idlist[i]
            
            dist = oid.calcDistance(id)
            # print("Dist: {0}\n".format(dist))
            if(dist < self.similardist):
                ret.append(i)
        
        return ret
    
    # проверяем ID по базе
    def checkid(self,id):
        similar = self.getSimilarObjects(id)
        return len(similar) == 0
    
    def getUserName(self,id):
        for u in users:
            if(u.id == id):
                return u.name
        return None
        
    # Добавить FaceId в базу   
    def addtobase(self,id):
        uid = self.detectuser(id)
        uiid = (uid.id) if uid is not None else 0
        
        id.uid = uid
        self.idlist.append(id)
        
        self.database.PushVisitor(id,uiid,1)
        
        if(uiid == 0):
            nuid = self.database.PushUserId(id)
            self.addnewuser(nuid, id)
        
        print("Add user to base: {0}".format(uiid))
        
        return uiid
