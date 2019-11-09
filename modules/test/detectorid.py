import numpy
import random
import math

class FaceId(object):
    id = []

    def __init__(self, id):
        self.id = id
        return
    
    def load(self, filename):
        self.id = numpy.load(filename)
    
    def save(self, filename):
        numpy.save(filename, self.id)
    
    # Расчёт расстояния между двумя векторами FaceId
    def calcDistance(self,id):
        sum = 0
        for i in (0, len(id.id) - 1):
            sum = sum + math.pow(id.id[i] - self.id[i], 2)
        return math.sqrt(sum)

class DetectorId(object):
    index = 0
    
    def __init__(self):
        self.index = 0
        # Инициализация детектора...
        return
    
    def generateRandId(self):
        id = []
        for i in (0, 49):
            id.append(random.randint(0, 1000) / 1000.0)
        return FaceId(id)
        
    def generateId(self, id):
        fid = FaceId(0)
        fid.load('config/data/{0}.npy'.format(id))
        
        return fid
    
    # frame: cv2::Mat
    def predict(self,frame,rois):
        ids = []
        self.index = self.index + 1
        for roi in rois:
            if(roi.id == 0):
                id = self.generateRandId()
            else:
                id = self.generateId(roi.id)
            
            ids.append(id)
            
        return ids
