import cv2
from cv2 import aruco
import BoardInfo
from GetSecondViewPoints import getCameraCoordinates
import os
import numpy as np


directories_to_use = [i for i in range(21)]
basePath = """../captures/Calib3/c_{0}/"""
outPathTemplate = """../camera_calibration_out/Calib3/c_{0}/"""
imgfmt = ".jpg"
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

    img = cv2.imread(path+"w"+imgfmt)

    if img is None:
        print("Skipping: "+path)
        continue

    validV = cv2.imread(path+"out_InvalidImageV.tiff", cv2.IMREAD_GRAYSCALE)
    validH = cv2.imread(path+"out_InvalidImageH.tiff", cv2.IMREAD_GRAYSCALE)
    coordsV = cv2.imread(path+"out_BinImageH.tiff", cv2.IMREAD_ANYDEPTH+cv2.IMREAD_GRAYSCALE)
    coordsH = cv2.imread(path+"out_BinImageV.tiff", cv2.IMREAD_ANYDEPTH+cv2.IMREAD_GRAYSCALE)


    corners, ids, rejected = aruco.detectMarkers(img, BoardInfo.aurcoDict)
    cimg = aruco.drawDetectedMarkers(img.copy(), corners, ids)

    cv2.imwrite(outPath+"DetectedMarkers.png", cimg)

    charucoCorners, charucoIds = [], []
    if len(ids) > 0:
        numCorners, charucoCorners, charucoIds = aruco.interpolateCornersCharuco(corners, ids, img, BoardInfo.charucoBoard)
    if len(charucoIds)<0:
        continue

    all_charco_corners_camera.append(charucoCorners.copy())
    all_charco_ids_camera.append(charucoIds.copy())

    cimg = aruco.drawDetectedCornersCharuco(img.copy(), charucoCorners, charucoIds)
    cv2.imwrite(outPath+"DetectedCorners.png", cimg)

    valid_points, new_points_cam, new_points_projector = getCameraCoordinates(img, validV, validH, coordsV, coordsH, charucoCorners)
    charucoIds = charucoIds[valid_points]

    if len(charucoIds)<0:
        continue

    all_charco_corners_camera_2.append(new_points_cam)
    all_real_points.append(BoardInfo.charucoBoard.chessboardCorners[charucoIds[:,0]])

    print(new_points_projector)
    all_charco_corners_projector.append(new_points_projector)
    all_charco_ids_projector.append(charucoIds)

camera_resolution = img.shape[:-1]

#CalibrationFlags=cv2.CALIB_ZERO_TANGENT_DIST + cv2.CALIB_FIX_K1 + cv2.CALIB_FIX_K2 + cv2.CALIB_FIX_K3
rep_err_camera, mtx_camera, dist_camera, rvecs_camera, tvecs_camera = cv2.aruco.calibrateCameraCharuco(all_charco_corners_camera, all_charco_ids_camera, BoardInfo.charucoBoard, camera_resolution, None, None, flags=cv2.CALIB_FIX_K2+cv2.CALIB_FIX_K3+cv2.CALIB_FIX_K4+cv2.CALIB_FIX_K5+cv2.CALIB_FIX_K6)
rep_err_proj, mtx_proj, dist_proj, rvecs_proj, tvecs_proj = cv2.aruco.calibrateCameraCharuco(all_charco_corners_projector, all_charco_ids_projector, BoardInfo.charucoBoard, projector_resolution, None, None, flags=cv2.CALIB_FIX_K2+cv2.CALIB_FIX_K3+cv2.CALIB_FIX_K4+cv2.CALIB_FIX_K5+cv2.CALIB_FIX_K6)

#np.savez("../camera_calibration_out/calculated_cams_matrix.npz", rep_err_camera=rep_err_camera, mtx_camera=mtx_camera, dist_camera=dist_camera , rvecs_camera=rvecs_camera, tvecs_camera=tvecs_camera, newcameramtx_camera=newcameramtx_camera, roi_camera=newcameramtx_camera,
 #        rep_err_proj=rep_err_proj, mtx_proj=mtx_proj, dist_proj=dist_proj, rvecs_proj=rvecs_proj, tvecs_proj=tvecs_proj, newcameramtx_proj=newcameramtx_proj, roi_proj=newcameramtx_proj)

retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = \
    cv2.stereoCalibrate(all_real_points, all_charco_corners_camera_2, all_charco_corners_projector,
                        mtx_camera, dist_camera, mtx_proj,
                        dist_proj, camera_resolution, flags=cv2.CALIB_FIX_INTRINSIC)

newcameramtx_camera, roi_camera=cv2.getOptimalNewCameraMatrix(cameraMatrix1,distCoeffs1,camera_resolution,1, camera_resolution)
newcameramtx_proj, roi_proj=cv2.getOptimalNewCameraMatrix(cameraMatrix2,distCoeffs2,projector_resolution,1, projector_resolution)

invCamMtx = np.linalg.inv(newcameramtx_camera)
invProjMtx = np.linalg.inv(newcameramtx_proj)


np.savez("../camera_calibration_out/calculated_cams_matrix_less_distortion.npz",
         retval=retval,
         cameraMatrix1=cameraMatrix1,
         distCoeffs1=distCoeffs1,
         cameraMatrix2=cameraMatrix2,
         distCoeffs2=distCoeffs2,
         R=R,
         T=T,
         E=E,
         F=F,
         newcameramtx_camera=newcameramtx_camera,
         roi_camera=roi_camera,
         newcameramtx_proj=newcameramtx_proj,
         roi_proj=roi_proj,
         invCamMtx=invCamMtx,
         invProjMtx=invProjMtx)


rep_err_camera, mtx_camera, dist_camera, rvecs_camera, tvecs_camera = cv2.aruco.calibrateCameraCharuco(all_charco_corners_camera, all_charco_ids_camera, BoardInfo.charucoBoard, camera_resolution, None, None)
rep_err_proj, mtx_proj, dist_proj, rvecs_proj, tvecs_proj = cv2.aruco.calibrateCameraCharuco(all_charco_corners_projector, all_charco_ids_projector, BoardInfo.charucoBoard, projector_resolution, None, None)


retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = \
    cv2.stereoCalibrate(all_real_points, all_charco_corners_camera_2, all_charco_corners_projector,
                        mtx_camera, dist_camera, mtx_proj,
                        dist_proj, camera_resolution, flags=cv2.CALIB_FIX_INTRINSIC)

newcameramtx_camera, roi_camera=cv2.getOptimalNewCameraMatrix(cameraMatrix1,distCoeffs1,camera_resolution,1, camera_resolution)
newcameramtx_proj, roi_proj=cv2.getOptimalNewCameraMatrix(cameraMatrix2,distCoeffs2,projector_resolution,1, projector_resolution)

invCamMtx = np.linalg.inv(newcameramtx_camera)
invProjMtx = np.linalg.inv(newcameramtx_proj)


np.savez("../camera_calibration_out/calculated_cams_matrix.npz",
         retval=retval,
         cameraMatrix1=cameraMatrix1,
         distCoeffs1=distCoeffs1,
         cameraMatrix2=cameraMatrix2,
         distCoeffs2=distCoeffs2,
         R=R,
         T=T,
         E=E,
         F=F,
         newcameramtx_camera=newcameramtx_camera,
         roi_camera=roi_camera,
         newcameramtx_proj=newcameramtx_proj,
         roi_proj=roi_proj,
         invCamMtx=invCamMtx,
         invProjMtx=invProjMtx)
