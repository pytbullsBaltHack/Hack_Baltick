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

    def __init__(self):
        # Инициализация детектора...
        pass

    def init(self, params):
        pass

    # frame: cv2::Mat
    def predict(self, frame, rois):
        ids = list()
        id = FaceId([i for i in range(50)])
        ids.append(id)
        return ids