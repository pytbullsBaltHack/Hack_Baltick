import cv2
import numpy
import math

from modules.database import Database

class FaceIdBase(object):
    # список id
    idlist = []
    
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
        idlist = []
        database = Database("server/id.sqlite3")
        similardist = 0.2
        return
    
    # Попробуем найти похожие id в базе, возвращаем индексы похожих
    def getSimilarObjects(self,id):
        ret = []
        
        for i in range(0, len(self.idlist)):
            oid = self.idlist[i]
            
            dist = oid.calcDistance(id)
            print("Dist: {0}\n".format(dist))
            if(dist < self.similardist):
                ret.append(i)
        
        return ret
    
    # проверяем ID по базе
    def checkid(self,id):
        similar = self.getSimilarObjects(id)
        return len(similar) == 0
    
    # Добавить FaceId в базу   
    def addtobase(self,id):
        self.idlist.append(id)
        
        return
