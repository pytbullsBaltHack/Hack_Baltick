import argparse
from sys import platform
from os import system
import gc
from utils.models import *
from utils.datasets import *
from utils.utils import *
from utils.xml_utils import *

import time
import datetime
import sqlite3

from torch.autograd import Variable

model = None
connection_SQLbase = None
SQLbase_filename = None

def load_net(opt):
    """
    Загрузка нейросети YOLOv3 как global
    :param opt: Main setting neuronetwork (path of cfg, weights, data and other)
    :return:
    """
    global model
    img_size = opt.img_size
    out, source, weights, half = opt.output, opt.source, opt.weights, opt.half
    device = torch_utils.select_device(opt.device)

    if (check_fpath(opt.cfg,)) & (check_fpath(weights)):
        model = Darknet(opt.cfg, img_size).cuda()
        if weights.endswith('.pt'):  # pytorch format
            model.load_state_dict(torch.load(weights, map_location=device)['model'])
            # model.load_state_dict(torch.load(model_Weights)['model'])
        else:  # darknet format
            _ = load_darknet_weights(model, weights)
        model.eval()
        # print(model)
        # model.to(model_device).eval()
        # Half precision
        half = opt.half and device.type != 'cpu'  # half precision only supported on CUDA
        if half:
            model.half()
        torch.backends.cudnn.benchmark = True  # set True to speed up constant image size inference
        return True
    else:
        return False

def open_videostream(opt):
    """
    Open videostream as global
    :param opt:
    :return:
    """
    try:
        return cv2.VideoCapture(opt.source)
    except:
        return None

def save_frame_xml(orig_frame, classes,  classids, confidences, boxes, out_dir):
    """
    Save original jpg, painting frame and xmlfile
    :param orig_frame:
    :param classes:
    :param classids:
    :param confidences:
    :param boxes:
    :param out_dir:
    :return:
    """
    now = datetime.datetime.now()
    base_file_name = f'{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}'
    output_path_jpg = os.path.join(out_dir, base_file_name + '.jpg')
    output_path_jpg_temp = os.path.join(out_dir, base_file_name + '_temp.jpg')
    output_path_xml = os.path.join(out_dir, base_file_name + '.xml')
    cv2.imwrite(output_path_jpg, orig_frame)

    #paint boxes of objects to frame
    for class_Id, conf_Id, box_Id in zip(classids, confidences, boxes):
        label = '%s %.2f' % (classes[int(class_Id)], conf_Id)
    cv2.imwrite(output_path_jpg_temp, cv2.resize(orig_frame, (int(orig_frame.shape[1]*0.5),
                                                              int(orig_frame.shape[0]*0.5))))
    # rename id_detected_class
    classids[:] = [classes[class_Id] for class_Id in classids]
    create_xml(output_path_xml, output_path_jpg, list(orig_frame.shape), classids, confidences, boxes)


def post_predict(pred, pred_img_shape, orig_img_shape, classes, show_classes):
    """
    Post prediction
    :param pred:
    :param pred_img_shape: Shape prediction image
    :param orig_img_shape: Shape original image
    :param classes: List all classes
    :param show_classes: List classes, which need show
    :return:
    """
    classIds = []
    confidences = []
    boxes = []
    for i, det in enumerate(pred):  # detections per image
        if det is not None and len(det):
            det[:, :4] = scale_coords(pred_img_shape[2:], det[:, :4], orig_img_shape).round()
            for *xyxy, conf, _, cls in det:
                if classes[int(cls)] in show_classes:
                    classIds.append(int(cls))
                    confidences.append(float(conf))
                    boxes.append(list(map(int, xyxy)))
    return classIds, confidences, boxes


def detect_video(opt, classes, show_classes, colors):
    """

    :param opt:
    :param classes:
    :param colors:
    :return:
    """
    global model, SQLbase_filename, connection_SQLbase
    vid = open_videostream(opt)
    if vid is None:
        print("videostream don't open")
        return -1
    device = torch_utils.select_device(opt.device)
    miss_frame = 0
    now = time.time()
    while (vid.isOpened()):
        if miss_frame > 10:
            break
        ret, img_ori = vid.read()
        if not ret:
            miss_frame += 1
            print('is not frame')
        else:
            miss_frame = 0
            if (time.time()-now) >= opt.wait_time:
                now_datetime = datetime.datetime.now()
                time_detect_frame = now_datetime.strftime("%Y-%m-%d %H:%M:%S")

                # Setting time diapason
                if (now_datetime.hour <= 9) or (now_datetime.hour >= 21):
                    # remove all files in end of day
                    remove_files(opt.output,  f'{now_datetime.year}-{now_datetime.month}-{now_datetime.day}')
                    now = time.time()
                    print('time is not to diapason')
                    continue
                if (now_datetime.weekday() >=5):
                    print("today is weekend, don't save today")

                # Convert frame to blob darknet
                img = [letterbox(img_ori, new_shape=opt.img_size, interp=cv2.INTER_LINEAR)[0]]
                img = np.stack(img, 0)
                img = img[:, :, :, ::-1].transpose(0, 3, 1, 2)  # BGR to RGB
                img = np.ascontiguousarray(img, dtype=np.float16 if opt.half else np.float32)  # uint8 to fp16/fp32
                img /= 255.0  # 0 - 255 to 0.0 - 1.0
                img = torch.from_numpy(img).to(device)
                if img.ndimension() == 3:
                    img = img.unsqueeze(0)
                pred = model(img)[0]
                if opt.half:
                    pred = pred.float()
                # Apply NMS
                pred = non_max_suppression(pred, opt.conf_thres, opt.nms_thres)
                classIds, confidences, boxes = post_predict(pred, img.shape, img_ori.shape, classes, show_classes)

                dict_detect_obj = {classes[int(i)]: classIds.count(i) for i in classIds}

                count_persons = 0 if not dict_detect_obj else dict_detect_obj['person']


                print(dict_detect_obj)

                now = time.time()
                if opt.view_img and dict_detect_obj:
                    if dict_detect_obj['person'] >= 3:
                        save_frame_xml(img_ori, classes, classIds, confidences, boxes, opt.output )
    vid.release()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-cfg', type=str, help='cfg file path')
    parser.add_argument('-classes', type=str, help='classes.names file path')
    parser.add_argument('-weights', type=str, help='path to weights file')
    parser.add_argument('-source', type=str, help='source')  # input file/folder, 0 for webcam
    parser.add_argument('-output', type=str, default='output/', help='output folder')  # output folder
    parser.add_argument('-img_size', type=int, default=416, help='inference size (pixels)')
    parser.add_argument('-conf-thres', type=float, default=0.2, help='object confidence threshold')
    parser.add_argument('-nms-thres', type=float, default=0.5, help='iou threshold for non-maximum suppression')
    parser.add_argument('-fourcc', type=str, default='mp4v', help='output video codec (verify ffmpeg support)')
    parser.add_argument('-half', action='store_true', help='half precision FP16 inference')
    parser.add_argument('-device', default='', help='device id (i.e. 0 or 0,1) or cpu')
    parser.add_argument('-view_img', action='store_true', help='display results')
    parser.add_argument('-show_classes', default='', type=str, help='file path show_classes.names')
    parser.add_argument('-wait_time', type=int, default=60, help='wait time of next frame (second) (default = 60 s)')
    opt = parser.parse_args()

    opt.cfg = '/media/vladimir/WORK/Pretrain_Models/YOLOv3_COCO_original/yolov3.cfg'
    opt.weights = '/media/vladimir/WORK/Pretrain_Models/YOLOv3_COCO_original/yolov3.weights'
    opt.classes = '/media/vladimir/WORK/Pretrain_Models/YOLOv3_COCO_original/coco.names'
    opt.source = '/media/vladimir/WORK/INCOEL_work/data/cam_2_12/Cam_12-2_2019.07.02_12-41-28.mp4'



    if opt.show_classes == '':
        opt.show_classes = opt.classes

    classes = read_list(opt.classes)
    show_classes = read_list(opt.show_classes)
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(classes))]

    now = datetime.datetime.now()
    SQLbase_filename = os.path.join(opt.output, f'{now.year}_{now.month}.db')


    with torch.no_grad():
        load_net(opt)
        gc.collect()
        if model is not None:
            while True:
                detect_video(opt, classes, show_classes, colors)

    system("pause")
