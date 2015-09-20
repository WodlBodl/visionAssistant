from backend import tagging, faceRecognition
from backend import textProcess
from hardware import _input
import thread
import subprocess
from multiprocessing import Pool
import time
import math

while True:
    ### Get button input ###
    if (_input.get_button() == True):
        _input.get_frame()
        print "Button Pressed"
        current_tags = []
        current_text = []
        ### Describe situation ###
        new_tags = tagging.tagImage("/home/pi/visionAssistant/frame.jpg")
        new_tags.extend(faceRecognition("/home/pi/visionAssistant/frame.jpg"))
        subprocess.call('convert frame.jpg frame.tiff', shell=True)
        subprocess.call('java -jar ocr.jar ~/visionAssistant/backend/ocr/Tess4J/lib/win32-x86 ~/visionAssistant/frame.tiff ~/visionAssistant/backend/ocr/Tess4J/tessdata ~/visionAssistant', shell=True)
        new_text = textProcess.textParse("/home/pi/visionAssistant/frame.tiff")
        new_text = []
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
        for tag in current_tags:
            subprocess.call('espeak -v en "'+str(tag)+'" &', shell=True)
        for word in current_text:
            subprocess.call('espeak -v en "'+str(word)+'" &', shell=True)
        if nothing in current_tags:
            subprocess.call('espeak -v en "Nothing new" &', shell = True)
