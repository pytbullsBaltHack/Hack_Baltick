import cv2
import numpy
import math
import os

# https://github.com/ageitgey/face_recognition/issues/43

from modules.debug import debugFrame
from modules.idbase import FaceIdBase
from modules.statistics import Statistic

#from modules.test.detectorface_mtcnn import DetectorFace, FaceRect
#from modules.test.detectorid_facenet import DetectorId, FaceId
from modules.detector_id.DetectoID import DetectorId, FaceId
from modules.Detector_Face.Detector_Face import DetectorFace

<<<<<<< HEAD
video_file = '/media/vladimir/WORK/data/camtemp.mp4'
cfg = '/media/vladimir/WORK/Pretrain_Models/YOLO_face/model-weights/cfg/yolov3-face.cfg'
weights = "/media/vladimir/WORK/Pretrain_Models/YOLO_face/model-weights/yolov3-wider_16000.weights"
classes_names = '/media/vladimir/WORK/Pretrain_Models/YOLO_face/model-weights/cfg/face.names'
img_size = 416
conf_thres = 0.2
nms_thres = 0.1
device = '0'

Detector_Face_params = {}
Detector_Face_params['cfg'] = cfg
Detector_Face_params['weights'] = weights
Detector_Face_params['img_size'] = img_size
Detector_Face_params['conf_thres'] = conf_thres
Detector_Face_params['nms_thres'] = nms_thres
Detector_Face_params['device'] = device
Detector_Face_params['classes_names'] = classes_names



=======
>>>>>>> 9ab329614b8bd9986adcbe7211731ef59bb914d5
class Processing(object):
    facedetector = False
    iddetector = False
    idbase = False
    statistics = Statistic
    frameid = 0
    
<<<<<<< HEAD
    def __init__(self):
        self.facedetector = DetectorFace(Detector_Face_params)
=======
    def __init__(self,cfg):
        self.frameid = 0
        self.facedetector = DetectorFace(cfg.facedet)
>>>>>>> 9ab329614b8bd9986adcbe7211731ef59bb914d5
        self.iddetector = DetectorId({})
        self.idbase = FaceIdBase()
        self.statistic = Statistic()
        
        return
        
    # Генерируем случайные файлы с ID 
    def initrandomfaceid(self):
        for i in range(0, 10):
            id = self.iddetector.generateRandId()
            id.save('config/data/{0}.npy'.format(i))
        return
        
    # Находим лица на кадре и возвращаем их список
    # Трекер тоже встроим сюда
    def detectFaces(self,frame):
        return self.facedetector(frame)

    # Определяем ID для всех лиц
    def detectId(self,frame,rects):
        return self.iddetector.predict(frame,rects)

    def saveCache(self,frameid,data):
        numpy.save('config/cache/{0}.npy'.format(frameid), data)
        return
        
    def loadCache(self,frameid):
        fn = 'config/cache/{0}.npy'.format(frameid)
        if(os.path.isfile(fn)):
            return numpy.load(fn, allow_pickle=True), True
        else:
            return False, False

    # Находим лица и определяем их ID:
    # возвращаем список объектов {"rect" : rect, "id": id}
    def detectAll(self,frame):
        cached, ret = self.loadCache(self.frameid)
        if(ret == True): return cached
    
        faces = self.detectFaces(frame)
        ids = self.detectId(frame, faces)

        all = []

        for id_faces, id_ids in zip (faces, ids):
            all.append({"rect" : id_faces, "id": id_ids})

        print(len(all))
        #
        # count = len(faces)
        #
        # if(count > 0):
        #     for i in (0, count - 1):
        #         rect = faces[i]
        #         id = ids[i]
        #
        #         # todo add mat roi
        #         all.append({"rect" : rect, "id": id})
        
        self.saveCache(self.frameid,all)
    
        return all
        
    def processFrame(self,frame):
        all = self.detectAll(frame)
<<<<<<< HEAD

        for id_all in all:
            f = id_all["rect"]
            id = id_all["id"]
            if (id.valid()):
                print("valid vector: {0}\n".format(len(id.id)))
                isnew = self.idbase.checkid(id)
                if (isnew):
                    self.idbase.addtobase(id)
                    self.statistic.increment()
        # count = len(all)
        # if(count > 0):
        #     for i in (0, count - 1):
        #         f = all[i]["rect"]
        #         id = all[i]["id"]
        #
        #
        #         if(id.valid()):
        #             print("valid vector: {0}\n".format(len(id.id)))
        #             isnew = self.idbase.checkid(id)
        #             if(isnew):
        #                 self.idbase.addtobase(id)
        #                 self.statistic.increment()
=======
        self.frameid = self.frameid + 1
        
        count = len(all)
        if(count > 0):
            for i in (0, count - 1):
                f = all[i]["rect"]
                id = all[i]["id"]
            
                if(id.valid()):
                    print("valid vector: {0}\n".format(len(id.id)))
                    isnew = self.idbase.checkid(id)
                    if(isnew):
                        self.idbase.addtobase(id)
                        self.statistic.increment()
>>>>>>> 9ab329614b8bd9986adcbe7211731ef59bb914d5
                
        self.debugStatisticModule(frame,all)
        return

    def debugStatisticModule(self, frame, all):
        drawframe = frame.copy()

        color = (0, 255, 0)
        for id_all in all:
            f = id_all['rect']
            text = "{0}".format(id_all['id'].id)
            cv2.putText(drawframe, text, (f.x + f.w, f.y + f.h), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1)
            cv2.rectangle(drawframe, (f.x, f.y), (f.x + f.w, f.y + f.h), color)


        # count = len(all)
        # if(count > 0):
        #     for i in (0, count - 1):
        #         f = all[i]["rect"]
        #         color = (0, 255, 0)
        #         # text = "{0}".format(f.id)
        #         text=''
        #         cv2.putText(drawframe, text, (f.x + f.w, f.y + f.h), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1)
        #         cv2.rectangle(drawframe, (f.x, f.y), (f.x + f.w, f.y + f.h), color)
                
        
        color = (0, 255, 0)
        text = "{0}".format(self.statistic.count)
        cv2.putText(drawframe, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1)
        
        color = (255, 0, 0)
        text = "{0}".format(self.frameid)
        cv2.putText(drawframe, text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1)
        
        debugFrame(drawframe)
        
    # Тестируем детектор -- он покажет окно с найденными объектами
    def debugDetector(self,frame):
        faces = self.detectFaces(frame)
        color = (0, 255, 0)
        drawframe = frame.copy()
        for f in faces:
            cv2.rectangle(drawframe, (f.x, f.y), (f.x + f.w, f.y + f.h), color)

        debugFrame(drawframe)
        
    # Тестируем детектор -- он покажет окно с найденными объектами и расстоянием до заданного id
    def debugDetectorId(self,frame,bid):
        all = self.detectAll(frame)
        
        baseid = self.iddetector.generateId(bid)
        
        drawframe = frame.copy()
        count = len(all)
        if(count > 0):
            for i in (0, count - 1):
                f = all[i]["rect"]
                id = all[i]["id"]
                if(id.valid()):
                    dist = baseid.calcDistance(id)
                    
                    if(dist < 0.2):
                        color = (0, 255, 0)
                    elif (dist < 0.4):
                        color = (0, 255, 255)
                    else:
                        color = (0, 0, 255)
                else:
                    color = (255, 0, 0)
                    
                cv2.rectangle(drawframe, (f.x, f.y), (f.x + f.w, f.y + f.h), color)
                
                text = "{0:.2f}".format(dist)
                cv2.putText(drawframe, text, (f.x + f.w, f.y + f.h), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1)
                
        debugFrame(drawframe)
        
