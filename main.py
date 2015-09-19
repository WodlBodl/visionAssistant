from backend import tagging
from hardware import _input
import thread
import time

frame_access = thread.allocate_lock()
request_description = False

def imaging_thread():
    while True:
        with frame_access:
            _input.get_frame()
        time.sleep(1)

def input_thread():
    while True:
        ### Get button and Ultrasonic input ###
        pass

def image_process_thread():
    if (request_description = True):
        with frame_access:
            ### Describe situation ###
            pass


thread.start_new_thread(imaging_thread(), ())
thread.start_new_thread(input_thread(), ())
