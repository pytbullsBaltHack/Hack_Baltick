class FaceId(object):
    id = []

    def __init__(self, id):
        self.id = id
        return
    
class DetectorId(object):

    def __init__(self):
        # Инициализация детектора...
        return
    
    def generateId(self):
        id = []
        for i in (0, 49):
            id.append(i)
        return id
    
    # frame: cv2::Mat
    def predict(self,frame,rois):
        ids = []
        for roi in rois:
            id = self.generateId()
            ids.append(id)
            
        return ids
