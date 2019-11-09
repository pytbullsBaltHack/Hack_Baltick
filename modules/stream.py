import cv2

class VideoStream(object):
    filename = ""
    
    def __init__(self,filename):
        self.filename = filename
        self.cap = cv2.VideoCapture(filename)
        
    def isOpened(self):
        return self.cap.isOpened()
    
    def read(self):
        return self.cap.read()

# config: Конфиг из config.getConfig()
def getStream(config):
    src = VideoStream(config.filename)
    
    return src