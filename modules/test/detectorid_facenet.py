import numpy
import random
import cv2
import math
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image, ImageDraw

# https://github.com/sesha997/Attendance-FaceRec
# https://github.com/timesler/facenet-pytorch
# https://github.com/davidsandberg/facenet
# https://www.jishuwen.com/d/25sg
# - https://medium.com/@seshasai_30381/a-very-simple-face-recognition-system-that-works-a62af612c8a6

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
    def valid(self):
        return len(self.id) > 10;
        
class DetectorId(object):
    index = 0
    resnet = False
    mtcnn = False
    
    def __init__(self):
        self.index = 0
        
        self.mtcnn = MTCNN(image_size=160)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval()
        # Инициализация детектора...
        return
    
    def opencvtopil(self,mat):
        mat = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
        return Image.fromarray(mat)
    
    def generateRandId(self):
        id = []
        for i in (0, 49):
            id.append(random.randint(0, 1000) / 1000.0)
        return FaceId(id)
        
    def generateId(self, id):
        fid = FaceId(0)
        fid.load('config/data/{0}.npy'.format(id))
        
        return fid
    
    def predict(self,frame,rois):
        ids = []
        
        for roi in rois:
            print("Size: {0}x{1}".format(roi.w,roi.h))
            if((roi.w > 39)&(roi.h > 39)):
                ROI = self.opencvtopil(frame[roi.y:roi.y+roi.h, roi.x:roi.x+roi.w]); 
                cropped = self.mtcnn(ROI)
            
                id = self.resnet(cropped.unsqueeze(0))
                print(id)
            else:
                id = []
            ids.append(FaceId(id))
        return ids
        