import os

def get_frame():
    os.system("fswebcam -d /dev/video1 -p YUYV frame.jpg")

def button():
    return False
