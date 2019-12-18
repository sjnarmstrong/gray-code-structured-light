from primesense import openni2
import numpy as np
import cv2
import os
from cv2 import aruco
import BoardInfo

base_storage_path = "../camera_calibration_out/Kinect"
second_dir = "calibImages_"
openni2.initialize("C:\Program Files\OpenNI2\Tools")

dirsInOutput = os.listdir(base_storage_path) if os.path.isdir(base_storage_path) else []

highest_i = -1
for f in dirsInOutput:
    if not os.path.isdir(f):
        continue
    try:
        test_i = int(f.replace("second_dir", ""))
    except:
        continue
    highest_i = max(highest_i, test_i)

save_path = base_storage_path+"/"+second_dir+str(highest_i+1)+"/"
os.makedirs(save_path, exist_ok=True)

all_charco_corners = []
all_charco_ids = []

detectorParams = aruco.DetectorParameters_create()
detectorParams.adaptiveThreshConstant = 5
detectorParams.adaptiveThreshWinSizeMin = 3
detectorParams.adaptiveThreshWinSizeMax = 50
detectorParams.adaptiveThreshWinSizeStep = 2
detectorParams.minMarkerPerimeterRate = 0.01
detectorParams.maxMarkerPerimeterRate = 8

TestAurcoDict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

def findPointsAndSaveImages(img, img_save_prefex, img_nr):
    imgName = img_save_prefex+str(img_nr)
    cv2.imwrite(save_path+imgName+".png", img)

    corners, ids, rejected = aruco.detectMarkers(img, BoardInfo.charucoBoard.dictionary)
    cimg = aruco.drawDetectedMarkers(img.copy(), corners, ids)
    cv2.imwrite(save_path+"detected__"+imgName+".png", cimg)

    if len(ids) < 10:
        return cimg, None, None
    numCorners, charucoCorners, charucoIds = aruco.interpolateCornersCharuco(corners, ids, img, BoardInfo.charucoBoard)
    cimg = aruco.drawDetectedCornersCharuco(img.copy(), charucoCorners, charucoIds)
    cv2.imwrite(save_path+"corners__"+imgName+".png", cimg)
    if numCorners <= 0:
        return cimg, None, None
    return cimg, charucoCorners, charucoIds



dev = openni2.Device.open_any()

#image_stream = dev.create_color_stream()
image_stream = dev.create_ir_stream()

image_stream.start()
image_frame = image_stream.read_frame()
image_frame_res = image_frame.height * image_frame.width

captureNum = 0
k=None
while k != ord('q'):
    image_frame = image_stream.read_frame()
    if image_stream.get_video_mode().pixelFormat == openni2.PIXEL_FORMAT_RGB888:
        image_to_process = np.array(image_frame.get_buffer_as_triplet()).reshape(image_frame.height, image_frame.width, -1)
        image_to_process[:,:,[0,2]]=image_to_process[:,:,[2,0]]
        image_to_process = image_to_process[..., ::-1, :]
    else:
        image_to_process = np.array(image_frame.get_buffer_as_uint8()).reshape(image_frame.height,
                                                                                   image_frame.width)
        image_to_process = image_to_process[..., :, ::-1]


    cv2.imshow("image",image_to_process)
    k = cv2.waitKey(30)
    if k == ord('c'):
        print("Would you like to keep this image press y for yes and n for no")
        k = cv2.waitKey(100)
        if k == ord('n'):
            continue

        rgb_img, rgb_corners, rgb_ids = findPointsAndSaveImages(image_to_process, "rgb__", captureNum)
        if rgb_corners is not None and rgb_ids is not None:
            all_charco_corners.append(rgb_corners)
            all_charco_ids.append(rgb_ids)
        captureNum += 1
        cv2.imshow("color", rgb_img)
        k = cv2.waitKey(1000)

image_stream.stop()


rep_err_camera, mtx_camera, dist_camera, rvecs_camera, tvecs_camera = cv2.aruco.calibrateCameraCharuco(all_charco_corners, all_charco_ids, BoardInfo.charucoBoard, (image_frame.height,
                                                                                                                                                                    image_frame.width), None, None)


np.savez("../camera_calibration_out/Kinect_ir_Mtx.npz",
         retval=rep_err_camera,
         cameraMatrix=mtx_camera,
         distCoeffs=dist_camera)
