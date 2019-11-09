class FaceRect(object):
    x = 0
    y = 0
    w = 0
    h = 0
    
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        return
    
class DetectorFace(object):

    def __init__(self):
        # Инициализация детектора...
        return
    
    # frame: cv2::Mat
    def predict(self,frame):
        rects = []
        rects.append(FaceRect(10, 10, 40, 40))
        
        return rects
