import subprocess
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

BUTTON = 16

GPIO.setup(BUTTON, GPIO.IN)

def get_frame():
    subprocess.call("fswebcam -d /dev/video0 --no-banner -p YUYV frame.jpg", shell=True)

def get_button():
    if GPIO.input(BUTTON):
        return False
    return True
