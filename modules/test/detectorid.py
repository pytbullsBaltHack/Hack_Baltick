class FaceId(object):
    id = []

    def __init__(self, id):
        self.id = id
        return
    
class DetectorId(object):
    index = 0
    
    def __init__(self):
        self.index = 0
        # Инициализация детектора...
        return
    
    def generateId(self, randv):
        id = []
        for i in (0, 49):
            id.append(i)
        id[0] = randv
        return id
    
    # frame: cv2::Mat
    def predict(self,frame,rois):
        ids = []
        self.index = self.index + 1
        for roi in rois:
            id = self.generateId(self.index)
            ids.append(id)
            
        return ids
