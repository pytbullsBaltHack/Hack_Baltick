import cv2
from facenet_pytorch import MTCNN
from PIL import Image, ImageDraw

# https://github.com/timesler/facenet-pytorch/blob/master/examples/face_tracking.ipynb

class FaceRect(object):
    x = 0
    y = 0
    w = 0
    h = 0
    id = 0
    
    def __init__(self, x, y, w, h, id):
        self.x = x if (x > 0) else 0
        self.y = y if (y > 0) else 0
        self.w = w if (w > 0) else 0
        self.h = h if (h > 0) else 0

        self.id = id
        return
        
    def rect(self):
        return (self.x,self.y,self.w,self.h)
        
class DetectorFace(object):
    frame = 0
    mtcnn = False
    
    def __init__(self,params):
        self.frame = 0
        self.mtcnn = MTCNN()
        
        # Инициализация детектора...
        return
    
    def isInRange(self,ffrom,fto):
        return ((self.frame >= ffrom) & (self.frame <= fto))
    
    def opencvtopil(self,mat):
        mat = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
        return Image.fromarray(mat)
    
    def __call__(self, frame):
        return self.predict(frame)
        
    # frame: cv2::Mat
    def predict(self,frame):
        rects = []
        boxes, _ = self.mtcnn.detect(self.opencvtopil(frame))
        if(boxes is not None):
            for b in boxes:
                rects.append(FaceRect(int(b[0]), int(b[1]), int(b[2] - b[0]), int(b[3] - b[1]), 0))

        return rects