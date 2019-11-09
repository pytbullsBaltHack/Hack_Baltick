import cv2
from sys import platform
from os import system
import gc


from . utils.models import *
from . utils.datasets import *
from . utils.utils import *


class FaceRect(object):
    id = 0
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def rect(self):
        return (self.x,self.y,self.w,self.h)
        

class DetectorFace:

    def __init__(self, param):
        # Инициализация детектора...
        self.cfg = param['cfg']
        self.weights = param['weights']
        self.classes_names =param['classes_names']
        self.img_size = param['img_size']
        self.device = torch_utils.select_device(param['device'] if torch.cuda.is_available() else 'cpu')
        self.conf_thres = param['conf_thres']
        self.nms_thres =param['nms_thres']

        self.model = Darknet(self.cfg, self.img_size)
        if torch.cuda.is_available():
            self.model.cuda()
        if self.weights.endswith('.pt'):  # pytorch format
            self.model.load_state_dict(torch.load(self.weights, map_location=self.device)['model'])
        else:  # darknet format
            _ = load_darknet_weights(self.model, self.weights)

        self.model.eval()

    # frame: cv2::Mat
    def __call__(self, frame):
        classIds = []
        confidences = []
        boxes = []

        #****processing frame*****
        img = [letterbox(frame, new_shape=self.img_size, interp=cv2.INTER_LINEAR)[0]]
        img = np.stack(img, 0)
        img = img[:, :, :, ::-1].transpose(0, 3, 1, 2)  # BGR to RGB
        img = np.ascontiguousarray(img, dtype= np.float32)
        img = img /255.0  # 0 - 255 to 0.0 - 1.0
        img = torch.from_numpy(img).to(self.device)

        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        #****processing frame*****

        #
        pred = self.model(img)[0]
        pred = non_max_suppression(pred, self.conf_thres, self.nms_thres)
        #
        classIds, confidences, boxes = post_predict(pred, img.shape, frame.shape)

        rects = []
        for xyxy in boxes:
            # plot_one_box(xyxy, frame, label='face', color=[0,0,0])
            rects.append(FaceRect(xyxy[0],xyxy[1],xyxy[2]-xyxy[0], xyxy[3]-xyxy[1]))
        # return rects, frame
        return rects
