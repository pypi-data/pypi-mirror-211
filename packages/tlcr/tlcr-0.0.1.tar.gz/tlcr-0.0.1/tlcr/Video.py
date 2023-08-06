import os
import cv2

os.environ['OPENCV_FFMPEG_DEBUG'] = '0'
os.environ['OPENCV_VIDEOIO_DEBUG'] = '0'


class Video:
    @staticmethod
    def fill_images(video_file, frames):
        cam = cv2.VideoCapture(video_file)
        frame_count = cam.get(cv2.CAP_PROP_FRAME_COUNT)
        for i in range(int(frame_count)):
            ret, frame = cam.read()
            if ret:
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    @staticmethod
    def get_video_duration(video_path):
        video = cv2.VideoCapture(video_path)
        frame = video.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = video.get(cv2.CAP_PROP_FPS)
        duration_in_seconds = frame / fps
        return duration_in_seconds
