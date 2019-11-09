
class FaceRect(object):
    x = 0
    y = 0
    w = 0
    h = 0
    id = 0
    
    def __init__(self, x, y, w, h, id):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.id = id
        return
        
class DetectorFace(object):

    def __init__(self):
        # Инициализация детектора...
        return
    
    # frame: cv2::Mat
    def predict(self,frame):
        rects = []
        rects.append(FaceRect(10, 10, 40, 40, 1))
        rects.append(FaceRect(80, 140, 60, 80, 2))
        
        return rects
