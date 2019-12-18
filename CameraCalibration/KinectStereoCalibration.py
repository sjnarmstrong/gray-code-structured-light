from primesense import openni2
import numpy as np
import cv2
import os
from cv2 import aruco
import BoardInfo

CalibAtribs = np.load("../camera_calibration_out/Kinect_ir_Mtx.npz")
ir_cameraMatrix=CalibAtribs["cameraMatrix"]
ir_distCoeffs=CalibAtribs["distCoeffs"]

CalibAtribs = np.load("../camera_calibration_out/Kinect_rgb_Mtx.npz")
rgb_cameraMatrix=CalibAtribs["cameraMatrix"]
rgb_distCoeffs=CalibAtribs["distCoeffs"]
openni2.initialize("C:\Program Files\OpenNI2\Tools")

dev = openni2.Device.open_any()

image_stream = dev.create_color_stream()
ir_stream = dev.create_ir_stream()

image_stream.start()
image_frame = image_stream.read_frame()
image_frame_res = image_frame.height * image_frame.width

all_charco_corners_camera, all_charco_corners_ir, all_real_points = [],[],[]

def detect_and_save_markers(rgb_img, ir_img):
    corners, ids, rejected = aruco.detectMarkers(rgb_img, BoardInfo.aurcoDict)
    if len(ids) < 5:
        return
    _, charucoCorners, charucoIds = aruco.interpolateCornersCharuco(corners, ids, rgb_img, BoardInfo.charucoBoard)
    if len(charucoIds)<5:
        return


    corners, ids, rejected = aruco.detectMarkers(ir_img, BoardInfo.aurcoDict)
    if len(ids) < 5:
        return
    _, charucoCorners_ir, charucoIds_ir = aruco.interpolateCornersCharuco(corners, ids, ir_img, BoardInfo.charucoBoard)
    if len(charucoIds_ir)<5:
        return

    selectionArray, selectionArray_ir, selected_ids = [], [], []

    for index, testId in enumerate(charucoIds):
        if testId not in charucoIds_ir:
            continue

        indexInIr = np.where(charucoIds_ir == testId)[0][0]
        selectionArray.append(index)
        selectionArray_ir.append(indexInIr)
        selected_ids.append(testId[0])

    if len(selected_ids) < 5:
        return
    all_charco_corners_camera.append(charucoCorners[selectionArray])
    all_charco_corners_ir.append(charucoCorners_ir[selectionArray_ir])
    all_real_points.append(BoardInfo.charucoBoard.chessboardCorners[selected_ids])

k=None

while k != ord('q'):
    image_frame = image_stream.read_frame()
    image_to_process = np.array(image_frame.get_buffer_as_triplet()).reshape(image_frame.height, image_frame.width, -1)
    image_to_process[:,:,[0,2]]=image_to_process[:,:,[2,0]]
    image_to_process = image_to_process[..., ::-1, :]

    cv2.imshow("image",image_to_process)
    k = cv2.waitKey(30)
    if k == ord('c'):

        print("Would you like to keep this image press y for yes and n for no")

        image_stream.stop()
        ir_stream.start()
        ir_frame = ir_stream.read_frame()
        ir_image_to_process = np.array(ir_frame.get_buffer_as_uint8()).reshape(ir_frame.height,
                                                                                  ir_frame.width)
        ir_image_to_process = ir_image_to_process[..., :, ::-1]
        ir_stream.stop()
        image_stream = dev.create_color_stream()
        image_stream.start()

        cv2.imshow("ir_image", ir_image_to_process)
        k = cv2.waitKey(2000)
        if k == ord('n'):
            continue
        detect_and_save_markers(image_to_process, ir_image_to_process)
        ir_stream = dev.create_ir_stream()


#retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = \
#    cv2.stereoCalibrate(all_real_points, all_charco_corners_camera, all_charco_corners_ir,
#                        rgb_cameraMatrix, rgb_distCoeffs, ir_cameraMatrix,
#                        ir_distCoeffs, (image_frame.height,image_frame.width), flags=cv2.CALIB_FIX_INTRINSIC)
retval, cameraMatrix2, distCoeffs2, cameraMatrix1, distCoeffs1, R, T, E, F = \
    cv2.stereoCalibrate(all_real_points, all_charco_corners_ir, all_charco_corners_camera,
                        ir_cameraMatrix, ir_distCoeffs, rgb_cameraMatrix, rgb_distCoeffs,
                        (image_frame.height, image_frame.width), flags=cv2.CALIB_FIX_INTRINSIC)

np.savez("../camera_calibration_out/calculated_Kinect_Stereo_matrix.npz",
         retval=retval,
         cameraMatrix1=cameraMatrix1,
         distCoeffs1=distCoeffs1,
         cameraMatrix2=cameraMatrix2,
         distCoeffs2=distCoeffs2,
         R=R,
         T=T,
         E=E,
         F=F)