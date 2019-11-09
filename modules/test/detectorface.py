
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
    frame = 0
    
    def __init__(self):
        self.frame = 0
        
        # Инициализация детектора...
        return
    
    def isInRange(self,ffrom,fto):
        return ((self.frame >= ffrom) & (self.frame <= fto))
    
    def __call__(self, frame):
        return self.predict(frame)
        
    # frame: cv2::Mat
    def predict(self,frame):
        rects = []
        
        if self.isInRange(1,30): rects.append(FaceRect(120, 200, 40, 40, 1))
        if self.isInRange(20,50):rects.append(FaceRect(10, 140, 60, 80, 2))
        if self.isInRange(40,80):rects.append(FaceRect(210, 10, 250, 180, 3))
        if self.isInRange(88,98): rects.append(FaceRect(120, 200, 40, 40, 1))
        
        if self.isInRange(120,190): rects.append(FaceRect(120+self.frame-120, 200, 40, 40, 4))
        
        if self.isInRange(210,280): rects.append(FaceRect(10, 120+self.frame-210, 60, 70, 5))
        self.frame = self.frame + 1
        
        return rects
