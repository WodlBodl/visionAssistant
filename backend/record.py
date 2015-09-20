import cv2
import indicoio
import numpy as np
import os
import time

featuresCacheFile = 'facialFeatures/faces'
indicoio.config.api_key = '043c49c2696176bd3d01015d8fb19fe3'

'''
This function creates an array of facial feature data and saves it
in the facialFeaturesData/ directory

Inputs:
    - directory, string, path to the directory where the face images are stored
    - nickname, string, name of the person whoes face it is
'''
def recordFaceData(directory, nickname):
    allImages = []
    count = 0

    for file in os.listdir(directory):
        if file.endswith('.jpg'):
            allImages.append(file)

    currentRecordedFeatures = {}
    currentRecordedFeatures['names'] = []
    currentRecordedFeatures['features'] = []

    print 'Caching...'
    for image in allImages:
        print 'Collecting info ... ', count
        count += 1

        face = indicoio.facial_localization(directory + '/' + image)
        if len(face) > 0:
            face = face[0]

            img = cv2.imread(directory + '/' + image)
            faceImg = img[
                face['top_left_corner'][1] : face['bottom_right_corner'][1],
                face['top_left_corner'][0] : face['bottom_right_corner'][0]
            ]

            facialFeatures = indicoio.facial_features(faceImg)

            if (count % 50) == 0:
                cv2.imwrite('images/faces/' + str(int(time.time())) + '.jpg', faceImg)

            currentRecordedFeatures['names'].append(nickname)
            currentRecordedFeatures['features'].append(facialFeatures)

    np.save(featuresCacheFile + nickname + '.npy', [currentRecordedFeatures])
    print 'Done'
    return currentRecordedFeatures

# recordFaceData('trainingData/mihai', 'Mihai')
# recordFaceData('trainingData/rishab', 'Rishab')
# recordFaceData('trainingData/pavel', 'Pavel')
# recordFaceData('trainingData/misha', 'Misha')
