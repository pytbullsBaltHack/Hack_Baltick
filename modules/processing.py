import cv2
import numpy

from modules.debug import debugFrame

from modules.test.detectorface import DetectorFace, FaceRect

class Processing(object):
    facedetector = False
    
    def __init__(self):
        self.facedetector = DetectorFace()
        return;

    # Находим лица на кадре и возвращаем их список
    # Трекер тоже встроим сюда
    def detectFaces(self,frame):
        return self.facedetector.predict(frame)

    def debugDetector(self,frame):
        faces = self.facedetector.predict(frame)
        
        color = (0, 255, 0)
        drawframe = frame.copy()
        for f in faces:
            cv2.rectangle(drawframe, (f.x, f.y), (f.w, f.h), color)
            
        debugFrame(drawframe)
        
