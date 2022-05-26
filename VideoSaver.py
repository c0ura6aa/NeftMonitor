import os
import time
import cv2


class VideoSaver:
    def __init__(self):
        self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.capture = cv2.VideoWriter()
        self.resolut = (0, 0)

    def create(self, resolut=(320, 240), fps=30, output='', time_ex=True):
        if self.capture.isOpened():
            return False

        name = os.path.splitext(output)
        if name == '':
            name = 'video'

        if time_ex:
            addons = time.strftime("%m%d%H%M%S", time.localtime())
            name = f'{name}-{addons}.mp4'
        else:
            name = f'{name}.mp4'
        print(f'Created video file {name}')
        self.capture = cv2.VideoWriter(name, self.fourcc, fps, resolut)
        self.resolut = resolut
        return True

    def close(self):
        if not self.capture.isOpened():
            return False
        self.capture.release()
        return True

    def write(self, img):
        if not self.capture.isOpened():
            return False

        h, w = img.shape
        if (self.resolut[0] != w) or (self.resolut[1] != h):
            self.capture.write(cv2.resize(img, self.resolut))
        else:
            self.capture.write(img)
        return True

    def __del__(self):
        self.close()
