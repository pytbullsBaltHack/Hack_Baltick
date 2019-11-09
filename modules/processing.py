import cv2
import numpy
import math

from modules.debug import debugFrame

from modules.test.detectorface import DetectorFace, FaceRect
from modules.test.detectorid import DetectorId, FaceId

class Processing(object):
    facedetector = False
    iddetector = False
    
    def __init__(self):
        self.facedetector = DetectorFace()
        self.iddetector = DetectorId()
        
        return
        
    def initrandomfaceid(self):
        for i in range(0, 10):
            id = self.iddetector.generateRandId()
            id.save('config/data/{0}.npy'.format(i))
        return
        
    # Находим лица на кадре и возвращаем их список
    # Трекер тоже встроим сюда
    def detectFaces(self,frame):
        return self.facedetector.predict(frame)

    def detectId(self,frame,rects):
        return self.iddetector.predict(frame,rects)

    # Расчёт расстояния между двумя векторами FaceId
    def calcDistance(self,ida,idb):
        sum = 0
        for i in (0, len(ida.id) - 1):
            sum = sum + math.pow(ida.id[i] - idb.id[i], 2)
        return math.sqrt(sum)

    # Тестируем детектор -- он покажет окно с найденными объектами
    def debugDetector(self,frame):
        faces = self.detectFaces(frame)
        color = (0, 255, 0)
        drawframe = frame.copy()
        for f in faces:
            cv2.rectangle(drawframe, (f.x, f.y), (f.x + f.w, f.y + f.h), color)

        debugFrame(drawframe)
        
    # Тестируем детектор -- он покажет окно с найденными объектами и расстоянием до заданного id
    def debugDetectorId(self,frame,bid):
        faces = self.detectFaces(frame)
        ids = self.detectId(frame, faces)
        
        baseid = self.iddetector.generateId(bid)
        
        drawframe = frame.copy()
        for i in (0, len(faces) - 1):
            f = faces[i]
            id = ids[i]
            dist = self.calcDistance(baseid, id)
            
            if(dist < 0.2):
                color = (0, 255, 0)
            elif (dist < 0.4):
                color = (0, 255, 255)
            else:
                color = (0, 0, 255)
            
            cv2.rectangle(drawframe, (f.x, f.y), (f.x + f.w, f.y + f.h), color)
            
            text = "{0}".format(dist)
            cv2.putText(drawframe, text, (f.x + f.w, f.y + f.h), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1)
            
        debugFrame(drawframe)
        
