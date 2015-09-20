import cv2
import indicoio
import numpy as np
import os
from sklearn import svm
# from sklearn.linear_model import SGDClassifier
# from sklearn.preprocessing import LabelEncoder
# from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.neighbors import KNeighborsClassifier
import time

indicoio.config.api_key = '043c49c2696176bd3d01015d8fb19fe3'
faceImgStorageDir = 'images/'

if not os.path.exists(faceImgStorageDir):
    os.makedirs(faceImgStorageDir)

lb = LabelEncoder()

def extractFaces(imgPath):
    faceArray = []
    faces = indicoio.facial_localization(imgPath)
    img = cv2.imread(imgPath)

    count = 0
    for face in faces:
        if (face['bottom_right_corner'][1] - face['top_left_corner'][1]) > (len(img[0]) * 0.2):
            count += 1
            faceImg = img[
                face['top_left_corner'][1] : face['bottom_right_corner'][1],
                face['top_left_corner'][0] : face['bottom_right_corner'][0]
            ]
            storageLocation = faceImgStorageDir + str(int(time.time())) + str(count) + '.jpg'
            cv2.imwrite(storageLocation, faceImg)
            faceArray.append(storageLocation)

    return faceArray

def identifyFaces(imgPath, testing=False):
    faces = extractFaces(imgPath)

    dataMisha = np.load('facialFeatures/facesMisha.npy')[0]
    dataMihai = np.load('facialFeatures/facesMihai.npy')[0]
    dataPavel = np.load('facialFeatures/facesPavel.npy')[0]
    dataRishab = np.load('facialFeatures/facesRishab.npy')[0]

    trainingNames = dataMisha['names'] + \
                    dataMihai['names'] + \
                    dataPavel['names'] + \
                    dataRishab['names']

    trainingFeatures = dataMisha['features'] + \
                    dataMihai['features'] + \
                    dataPavel['features'] + \
                    dataRishab['features']

    n_trainingNames = lb.fit_transform(trainingNames)

    # clf = SGDClassifier(loss="modified_huber", penalty="l1")
    # clf = SGDClassifier(loss="modified_huber", penalty="l1", epsilon=0.0001)
    # clf = NearestCentroid()
    clf = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None)

    clf.fit(trainingFeatures, n_trainingNames)
    for path in faces:
        print lb.inverse_transform(clf.predict(indicoio.facial_features(path)))

    if testing == True:
        predictedNames = []
        trainingNames = dataMisha['names'][0:650] + \
                        dataMihai['names'][0:650] + \
                        dataPavel['names'][0:650] + \
                        dataRishab['names'][0:650]

        trainingFeatures = dataMisha['features'][0:650] + \
                        dataMihai['features'][0:650] + \
                        dataPavel['features'][0:650] + \
                        dataRishab['features'][0:650]

        testNames = dataMisha['names'][651:701] + \
                        dataMihai['names'][651:701] + \
                        dataPavel['names'][651:701] + \
                        dataRishab['names'][651:701]

        testFeatures = dataMisha['features'][651:701] + \
                        dataMihai['features'][651:701] + \
                        dataPavel['features'][651:701] + \
                        dataRishab['features'][651:701]

        correctCount = 0
        count = 0

        for x in range(0,len(testFeatures)):
            predictedName = clf.predict(testFeatures[x])
            predictedNames.append(predictedName)

        predictedNames = lb.inverse_transform(predictedNames)

        for x in range(0,len(predictedNames)):
            print count , ' *** ', predictedNames[x], ' - ', testNames[x]
            count += 1
            if predictedNames[x] == testNames[x]:
                correctCount += 1

        print 'Correct % - ', (correctCount / float(len(predictedNames))) * 100
        print correctCount, '/' , len(predictedNames)
