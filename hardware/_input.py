import os
from RPi.GPIO import GPIO

GPIO.setmode(GPIO.BOARD)

BUTTON = 16

GPIO.setup(BUTTON, GPIO.IN)

def get_frame():
    os.system("fswebcam -d /dev/video1 --no-banner -p YUYV frame.jpg")

def button():
    if GPIO.input(BUTTON):
        return False
    return True
