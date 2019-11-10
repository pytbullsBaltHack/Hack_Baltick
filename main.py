import os
import numpy
import cv2

from modules.config import getConfig
from modules.stream import getStream
from modules.debug  import debugFrame
from modules.processing import Processing

def init():
    
    return
    
def main():
    # Получаем конфиг запуска из абстрактного источника 
    # (сейчас это ini, потом параметры от другого приложения или из БД)
    cfg = getConfig()
    if(cfg == False):
        print("Could not load config")
        return
    
    # Инициализация нейронок и всего остального
    init()
    
    # Запускаем стрим через конфиг 
    # (по сути, это обёрнутый cv2.VideoCapture, он доступен через stream.cap)
    stream = getStream(cfg)
    
    # Объект, где происходит обработка кадра: детект лиц, трекинг, идентификация
    processing = Processing(cfg)
    
    if (stream.isOpened()== False): 
        print("Error opening video stream or file")
        return

    #Запись видео

    out = cv2.VideoWriter('output.avi', -1, 20.0, (1280, 720))


    # Читаем всё видео
    while(stream.isOpened()):
        ret, frame = stream.read()
        if ret == True:
            #processing.debugDetectorId(frame, 2)
            processing.processFrame(frame)
            out.write(frame)


            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
 
        # Break the loop
        else: 
            break

# Точка входа     
main()