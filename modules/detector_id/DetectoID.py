from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import cv2
import os
import math
from PIL import Image, ImageDraw
import random
import numpy as np
# from scipy.spatial import distance
from fastdtw import fastdtw

workers = 0 if os.name == 'nt' else 4

"""
@author Alexey_B
@brief Class for calculate ID
"""

class FaceId(object):
    id = []
    uid = None
    registered = False
    
    def __init__(self, id):
        self.id = id
        self.uid = None
        self.registered = False
        return

    # Расчёт расстояния между двумя векторами FaceId
    def calcDistance(self,id):
        mas_id_1 = id.id
        mas_id_2 = self.id
        # mas_id_1 = id.id.detach().cpu()
        # mas_id_2 = self.id.detach().cpu()
        # distance, path = fastdtw(mas_id_1, mas_id_2)
        # return distance
        dist = (mas_id_1 - mas_id_2) ** 2
        dist = dist.sum()
        dist = pow(dist, 0.5)
        # dists = [[(e1 - e2).norm().item() for e2 in mas_id_1] for e1 in mas_id_2]

        return dist

        # sum = 0
        # for i in (0, len(id.id) - 1):
        #     sum = sum + math.pow(id.id[i] - self.id[i], 2)
        #
        # return math.sqrt(sum)
    
    def valid(self):
        return len(self.id) > 10;
    def tostring(self):
        stra  = ["{0:0.6}".format(float(x)) for x in self.id]
        ret = ','.join(stra)
        return ret
        
class DetectorId(object):

    def __init__(self, param):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        #self.device = torch.device('cpu')
        self.mtcnn = MTCNN(image_size=160, device = self.device)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)

    def opencv_to_pil(self, mat):
        mat = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
        return Image.fromarray(mat)

    def generate_randId(self):
        id = []
        for i in (0, 49):
            id.append(random.randint(0, 1000) / 1000.0)
        return FaceId(id)

    def generate_id(self, id):
        fid = FaceId(0)
        fid.load('config/data/{0}.npy'.format(id))

        return fid

    # frame: cv2::Mat
    def predict(self, frame, rois):
        ids = []
        for roi in rois:
            # print("Size: {0}x{1} {2},{3}".format(roi.w, roi.h, roi.x, roi.y))
            # print('Relation wh: ', (roi.w / roi.h))

            if (roi.w > 99) & (roi.h >99):
                ROI = self.opencv_to_pil(frame[roi.y:roi.y + roi.h, roi.x:roi.x + roi.w]);

                if torch.cuda.is_available():

                    cropped = self.mtcnn(ROI)
                    if (cropped is not None):
                        aligned = []
                        aligned.append(cropped)
                        temp = torch.stack(aligned).to(self.device)
                        id = self.resnet(temp).detach().cpu()
                    else:
                        id = [[]]
                else:
                    cropped = self.mtcnn(ROI)
                    if(cropped is not None):
                        id = self.resnet(cropped.unsqueeze(0))
                    else:
                        id = [[]]
            else:
                id = [[]]
            ids.append(FaceId(id[0]))
        return ids
