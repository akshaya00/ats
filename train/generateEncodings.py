from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
from initializers import createEncodingsFile

#function to create encodings from images in dataset
def generateEncodingsFromImages(directoryPath):

    #backups old encodings file and generates new encodings
    createEncodingsFile('../encodings'+'/'+str(directoryPath.split('/',2)[2]))

    imagePaths = list(paths.list_images(directoryPath))

    # initialize the list of known encodings and known names
    knownEncodings = []
    knownNames = []

    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        name = imagePath.split(os.path.sep)[-2]

        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb,model='cnn')

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            knownNames.append(name)

    # dump the facial encodings + names to disk
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open('../encodings'+'/'+str(directoryPath.split('/',2)[2])+'/'+'encodings.pickle', "wb")
    f.write(pickle.dumps(data))
    f.close()


"""
test script for generateEncodingsFromImages

generateEncodingsFromImages('../data/strw239/7-C')
"""
generateEncodingsFromImages('../data/strw239/7-C')
