
import cv2
from sys import platform
from os import system
import gc
from modules.Detector_Face.utils import utils
from modules.Detector_Face.utils import torch_utils
import torch
from modules.Detector_Face.Detector_Face import *
# import . Detector_Face


video_file = '/media/vladimir/WORK/INCOEL_work/data/cam_2_12/Cam_12-2_2019.07.02_12-41-28.mp4'
cfg = '/media/vladimir/WORK/Pretrain_Models/YOLOv3_COCO_original/yolov3.cfg'
weights = '/media/vladimir/WORK/Pretrain_Models/YOLOv3_COCO_original/yolov3.weights'
classes_names = '/media/vladimir/WORK/Pretrain_Models/YOLOv3_COCO_original/coco.names'

video_file = '/media/vladimir/WORK/data/test2.mp4'
cfg = '/media/vladimir/WORK/Pretrain_Models/YOLO_face/model-weights/cfg/yolov3-face.cfg'
weights = "/media/vladimir/WORK/Pretrain_Models/YOLO_face/model-weights/yolov3-wider_16000.weights"
classes_names = '/media/vladimir/WORK/Pretrain_Models/YOLO_face/model-weights/cfg/face.names'

img_size = 416
conf_thres = 0.2
nms_thres = 0.1
device = '0'

param ={}
param['cfg']=cfg

param = {}
param['cfg'] = cfg
param['weights'] = weights
param['img_size'] = img_size
param['conf_thres'] = conf_thres
param['nms_thres'] = nms_thres
param['device'] = device
param['classes_names'] = classes_names


model = None
device = torch_utils.select_device(param['device'])


print(param)

model_Net = DetectorFace(param)

torch.backends.cudnn.benchmark = True
gc.collect()


cap = cv2.VideoCapture(video_file)      #для последующего автоматического перебора файлов


while(cap.isOpened()):
    ret, frame = cap.read()             #получаем кадр из видеопотока
    if frame is None:                   #проверка на корректность кадра
        break

    pred, frame = model_Net(frame)
    # pred = model_Net(frame)
    print(pred)

    cv2.imshow("video_frame", frame)    #показываем кадр в opencv окне
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break                           #в случае нажатия клавиши q выходим из цикла
cap.release()
cv2.destroyAllWindows()