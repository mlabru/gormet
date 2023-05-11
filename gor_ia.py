# -*- coding: utf-8 -*-
"""
gor_ia

2023.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging

# numPy
import numpy as np

# openCV
import cv2

# imutils
import imutils

# local
import gor_defs as df

# < constants >--------------------------------------------------------------------------------

# initialize the list of class labels MobileNet SSD was trained to detect...
D_CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car",
             "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person",
             "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# ...then generate a set of bounding box colors for each class
D_COLORS = np.random.uniform(0, 255, size=(len(D_CLASSES), 3))

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def load_model(f_args):
    """
    create a database connection to the SQLite database specified by fs_file_db

    :param f_args: args
    """
    # load serialized model from disk
    print("[INFO] loading model...")

    # return model
    return cv2.dnn.readNetFromCaffe(f_args.proto, f_args.model)

# ---------------------------------------------------------------------------------------------
def detect(f_model, f_confidence, f_frame):
    """
    create a database connection to the SQLite database specified by fs_file_db

    :param f_frame: frame
    """
    # resize frame
    l_frame = imutils.resize(f_frame, width=400)

    # grab the frame dimensions
    (h, w) = l_frame.shape[:2]

    # convert to a blob
    l_blob = cv2.dnn.blobFromImage(cv2.resize(l_frame, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and predictions
    f_model.setInput(l_blob)
    # obtain the detections and predictions
    detections = f_model.forward()

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is greater than the minimum confidence
        if confidence > f_confidence:
            # extract the index of the class label from the `detections`
            idx = int(detections[0, 0, i, 1])
            # then compute the (x, y)-coordinates of the bounding box for the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the prediction on the frame
            label = "{}: {:.2f}%".format(D_CLASSES[idx], confidence * 100)
            cv2.rectangle(l_frame, (startX, startY), (endX, endY), D_COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(l_frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, D_COLORS[idx], 2)

# < the end >----------------------------------------------------------------------------------
