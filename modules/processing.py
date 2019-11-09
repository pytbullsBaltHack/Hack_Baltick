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
        return;

    # Находим лица на кадре и возвращаем их список
    # Трекер тоже встроим сюда
    def detectFaces(self,frame):
        return self.facedetector.predict(frame)

    def detectId(self,frame,rects):
        return self.iddetector.predict(frame,rects)

    # Расчёт расстояния между двумя векторами FaceId
    def calcDistance(self,ida,idb):
        sum = 0
        for i in (0, len(ida) - 1):
            sum = sum + math.pow(ida[i] - idb[i], 2)
        return math.sqrt(sum)

    # Тестируем детектор -- он покажет окно с найденными объектами
    def debugDetector(self,frame):
        faces = self.detectFaces(frame)
        ids = self.detectId(frame, faces)
        
        baseid = self.iddetector.generateId(122)
        
        color = (0, 255, 0)
        drawframe = frame.copy()
        for i in (0, len(faces) - 1):
            f = faces[i]
            id = ids[i]
            dist = self.calcDistance(baseid, id)
            cv2.rectangle(drawframe, (f.x, f.y), (f.x + f.w, f.y + f.h), color)
            
            text = "{0}".format(dist)
            cv2.putText(drawframe, text, (f.x + f.w, f.y + f.h), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1)
            
        debugFrame(drawframe)
        
