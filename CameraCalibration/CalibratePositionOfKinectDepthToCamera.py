import cv2
from cv2 import aruco
import BoardInfo
from GetSecondViewPoints import getCameraCoordinates
import os
import numpy as np


directories_to_use = [i for i in range(21)]
basePath = """../captures/Calib3/c_{0}/"""
outPathTemplate = """../camera_calibration_out/Calib3/c_{0}/"""
projector_resolution =(1024, 768)

all_charco_corners_camera = []
all_charco_corners_camera_2 = []
all_charco_corners_projector = []
all_charco_ids_camera = []
all_charco_ids_projector = []

all_real_points = []

for dirnum in directories_to_use:
    path = basePath.format(dirnum)
    outPath = outPathTemplate.format(dirnum)
    os.makedirs(outPath, exist_ok=True)

    img_camera = cv2.imread(path+"w.jpg")
    img_kinect = cv2.imread(path+"kinect___rgb.png")

    if img_kinect is None:
        print("Skipping: "+path)
        continue


    #corners, ids, rejected = aruco.detectMarkers(img_kinect, BoardInfo.aurcoDict)
    #cimg = aruco.drawDetectedMarkers(img_kinect.copy(), corners, ids)
    retval, corners = cv2.findChessboardCorners(img_camera, (10,14))
    cimg = cv2.drawChessboardCorners(img_camera.copy(), (10,14), corners, True)
    print(retval)
    cv2.imshow("tset", cimg)
    cv2.waitKey(0)

