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
        
        fid = eval('[' + dbitem[1] + ']')
        tensor = torch.tensor(fid, dtype=torch.float32, requires_grad=True)
        self.face_id = FaceId(tensor)
        self.name = dbitem[2]
        
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
    similardist = 0.55
    
    # TODO: для оптимизации обеспечивать кластеризацию, 
    # т.е. при поиске сохранять результаты о похожести
    # чтобы не искать через кучу дублирующихся объектов
    
    # TODO: обеспечить выгрузку в базу старых лиц
    
    def __init__(self):
        self.idlist = []
        self.visitors = []
        self.database = Database("server/db.sqlite3")
        self.similardist = 0.55
        self.loadusers()
        return 
   
    def loadusers(self):
        users = self.database.GetUserList()
        #print(users)
        for u in users:
            ur = UserRecord()
            ur.parse(u)
            self.visitors.append(ur)
            #print('added user {0}\n'.format(ur.name))
            #print(ur.face_id)
        return
    def detectuser(self,id):
        mindist = self.similardist
        minuser = None
        for v in self.visitors:
            dist = id.calcDistance(v.face_id)
            #print(id.id)
            #print(v.face_id.id)
            print("Dist: {0} to {1}".format(dist,v.id))
            if (dist < mindist):
                #print("Select user: {0}: {1}".format(v.id,dist))
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
    
    def checkvisitor(self,id):
        similar = self.getSimilarObjects(id)
        
        return len(similar) == 0
    
    # проверяем ID по базе
    def checkid(self,id):
        #print("users length: {0}".format(len(self.visitors)))
        uid = self.detectuser(id)
        uuid = (uid.id) if uid is not None else None
        
        return uuid
    
    def getUserName(self,id):
        for u in self.visitors:
            if(u.id == id):
                return u.name
        return "Unknown"
        
    def addvisitor(self,id,uuid):
        if(uuid is not None):
            self.idlist.append(id)
            self.database.PushVisitor(id,uuid,1)
        
    # Добавить FaceId в базу   
    def addtobase(self,id):
        uuid = self.database.PushUserId(id)
        self.addnewuser(uuid, id)
        
        print("Add user to base: {0}".format(uuid))
        
        return uuid
