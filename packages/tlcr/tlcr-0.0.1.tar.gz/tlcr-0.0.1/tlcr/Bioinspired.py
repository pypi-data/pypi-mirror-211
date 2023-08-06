import os
import cv2
from tlcr.Video import Video


class Bioinspired:
    def __init__(self, width, height, path_to_save):
        self.__retina = cv2.bioinspired_Retina.create((width, height))
        self.__retina.write('retinaParams.xml')
        self.__retina.setup('retinaParams.xml')
        self.__orig = 'orig'
        self.__res = 'res'
        self.__path_orig = os.path.join(path_to_save, self.__orig)
        self.__path_res = os.path.join(path_to_save, self.__res)
        if not os.path.exists(self.__path_orig):
            os.makedirs(self.__path_orig)
        if not os.path.exists(self.__path_res):
            os.makedirs(self.__path_res)

    def run(self, url):
        path_orig = os.path.join(self.__path_orig, os.path.splitext(os.path.basename(url))[0])
        path_res = os.path.join(self.__path_res, os.path.splitext(os.path.basename(url))[0])
        images = []
        Video.fill_images(url, images)
        images = images[::5]
        size = len(images)

        for i in range(0, size):
            frame = images[i]
            self.__retina.run(frame)
            res = self.__retina.getMagno()
            frame_path = '{}_{}.jpg'.format(path_orig, i)
            res_path = '{}_{}.jpg'.format(path_res, i)
            print(frame_path, res_path)
            if not cv2.imwrite(frame_path, frame):
                break
            cv2.imwrite(res_path, res)

