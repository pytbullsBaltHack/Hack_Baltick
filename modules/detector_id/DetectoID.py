from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import cv2
import os
import math
from PIL import Image, ImageDraw
import random

workers = 0 if os.name == 'nt' else 4

"""
@author Alexey_B
@brief Class for calculate ID
"""


class FaceId(object):
    id = []

    def __init__(self, id):
        self.id = id
        return

    # Расчёт расстояния между двумя векторами FaceId
    def calcDistance(self,id):
        sum = 0
        for i in (0, len(id.id) - 1):
            sum = sum + math.pow(id.id[i] - self.id[i], 2)
        return math.sqrt(sum)
    def valid(self):
        return len(self.id) > 10;

class DetectorId(object):

    def __init__(self, param):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        # self.device = torch.device('cpu')
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


        # for roi in rois:
        #     id = []
        #     ids.append(FaceId(id))

        for roi in rois:
            #print("Size: {0}x{1}".format(roi.w, roi.h))
            if (roi.w > 39) & (roi.h > 39):
                ROI = self.opencv_to_pil(frame[roi.y:roi.y + roi.h, roi.x:roi.x + roi.w])
                if torch.cuda.is_available():
                    try:
                        cropped = self.mtcnn(ROI)
                        aligned = []
                        aligned.append(cropped)
                        temp = torch.stack(aligned).to(self.device)
                        id = self.resnet(temp).detach().cpu()
                    except:
                        id = []
                else:
                    cropped = self.mtcnn(ROI).unsqueeze(0)
                    id = self.resnet(cropped)
<<<<<<< HEAD


                # # cropped = self.mtcnn(ROI).unsqueeze(0)
                # cropped = self.mtcnn(ROI)
                # aligned = []
                # aligned.append(cropped)
                # # cropped = cropped.to(self.device)
                # # id = self.resnet(cropped)
                # temp = torch.stack(aligned).to(self.device)
                # id = self.resnet(temp).detach().cpu()

=======
>>>>>>> 9ab329614b8bd9986adcbe7211731ef59bb914d5
            else:
                id = [[]]
            ids.append(FaceId(id[0]))
        return ids
