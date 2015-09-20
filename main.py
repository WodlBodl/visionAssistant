from backend import tagging, faceRecognition, textProcess
from hardware import _input
import thread
import time
import os
import math

frame_access = thread.allocate_lock()
sound_output_access = thread.allocate_lock()
request_description = False

def imaging_thread():
    while True:
        with frame_access:
            _input.get_frame()
        time.sleep(1)

def input_thread():
    while True:
        ### Get button input ###
        if (get_button() == True):
            request_description = True
            print "Button Pressed"
        else:
            request_description = False


def image_process_thread():
    current_tags = []
    current_text = []
    while True:
        if (request_description == True):
            with frame_access:
                ### Describe situation ###
                new_tags = []
                new_text = []
                new_tags = tagging.tagImage("/home/pi/visionAssistant/frame.jpg")
                new_tags.extend(faceRecognition("/home/pi/visionAssistant/frame.jpg"))
                text = textProcess.textParse("/home/pi/visionAssistant/frame.jpg")
                if (len(new_tags)-len(current_tags)) < 3:
                    same = []
                    for tag in current_tags:
                        if tag in new_tags:
                            same.append(new_tags.index(tag))
                    if abs(len(new_tags) - len(same)) > 3:
                        for index in same:
                            del new_tags[index]
                current_tags = new_tags
                if (len(new_text)-len(current_text)) < 1:
                    same = []
                    for word in current_text:
                        if word in new_text:
                            same.append(new_text.index(word))
                    if abs(len(new_text) - len(same)) > 3:
                        for index in same:
                            del new_text[index]
                current_text = new_text
                current_tags = new_tags
            for tag in current_tags:
                os.system('espeak -v en "'+str(tag)+'"')
            for word in current_text:
                os.system('espeak -v en "'+str(word)+'"')
            if nothing in current_tags:
                os.system('espeak -v en "Nothing new"')



thread.start_new_thread(imaging_thread(), ())
thread.start_new_thread(input_thread(), ())
thread.start_new_thread(image_process_thread(), ())
