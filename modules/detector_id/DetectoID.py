from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torch.utils.data import DataLoader
from torchvision import datasets
import numpy as np
import pandas as pd
import os

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


class DetectorId(object):

    def __init__(self, param):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)


    # frame: cv2::Mat
    def predict(self, frame, rois):
        aligned = self.prepare_data(frame, rois)
        embeddings = self.model(aligned).detach().cpu()
        ids = self.post_data(embeddings)
        return ids