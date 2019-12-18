import numpy as np
from open3d import open3d
import os
import cv2
import struct

imgfmt = ".jpg"
baseReadPath = "../captures/"
datasets = ["Statue", "Calib3", "Cup", "DragonParty", "Punch", "ToyCar"]
open_ni_path = "C:\Program Files\OpenNI2\Tools"

CalibAtribs = np.load("../camera_calibration_out/calculated_Kinect_Stereo_matrix.npz")
retval = CalibAtribs["retval"]
rgbMtx = CalibAtribs["cameraMatrix1"]
distRgb = CalibAtribs["distCoeffs1"]
irMtx = CalibAtribs["cameraMatrix2"]
distIr = CalibAtribs["distCoeffs2"]
R = CalibAtribs["R"]
T = CalibAtribs["T"]
E = CalibAtribs["E"]

T_mtx_T_old = np.array([[0.999, -0.036, -0.032, 308.597],
                    [0.036, 0.999, 0.008, -3.948],
                    [0.032, -0.009, 0.999, -130.367],
                    [0, 0, 0, 1]]).T
T_mtx_T_2 = np.array([[0.998, 0.036, -0.045, 30.147],
                      [-0.038, 0.998, -0.042, 40.000],
                      [0.043, 0.044, 0.998, -6.944],
                      [0,0,0,1]])
T_mtx_T = np.array([[ 9.96858000e-01,  4.41000000e-04, -7.66030000e-02,
         3.43851193e+02],
       [-3.37800000e-03,  9.98748000e-01, -3.27580000e-02,
         2.98086240e+01],
       [ 7.64770000e-02,  3.34260000e-02,  9.95978000e-01,
        -1.23954307e+02],
       [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
         1.00000000e+00]]).T

for dataset in datasets:
    for captureFolder in os.listdir(baseReadPath + dataset):
        if not os.path.isdir(baseReadPath + dataset + "/" + captureFolder):
            continue
        path = baseReadPath + dataset + "/" + captureFolder + "/"
        depth_img = cv2.imread(path + "kinect___Depth.tiff", cv2.IMREAD_GRAYSCALE + cv2.IMREAD_ANYDEPTH).astype(
            np.float64)

        color_img = cv2.imread(path + "kinect___rgb.png").astype(np.float64) / 255

        # depth_img_in_mm = 1000 / (depth_img * -0.0030711016 + 3.3309495161)
        depth_img_in_mm = depth_img
        depth_img_in_mm[np.where(depth_img >= 2047)] = 0

        indImg = np.indices((480, 640)).reshape(2, -1)
        depth_img_in_mm = depth_img_in_mm.reshape(-1)

        indImg[[0, 1]] = indImg[[1, 0]]
        indImg = indImg.T.astype(np.float64)

        points = cv2.convertPointsToHomogeneous(cv2.undistortPoints(indImg[None,], irMtx, distIr))[:, 0].T
        points *= depth_img_in_mm
        points = points.T[np.where(points[2] > 10)]
        imagePoints = cv2.projectPoints(points, R, T, rgbMtx, distRgb)[0][:, 0]
        imagePoints = np.clip(np.rint(imagePoints), [0, 0], [640 - 1, 480 - 1]).astype(np.int32)
        colors = color_img[imagePoints[:, 1], imagePoints[:, 0]]

        # color_inds = [[openni2.convert_depth_to_color(depth_stream, color_stream, i, j, depth_img[j, i])
        #               for i in range(640)] for j in range(480)]
        # points = np.array(points).reshape(-1, 3)*[1,1,-1]
        # color_inds = np.clip(np.array(color_inds).reshape(-1, 2), [0, 0], [640 - 1, 480 - 1])
        # colors = color_img[color_inds[:, 1], color_inds[:, 0]]

        points = np.dot(cv2.convertPointsToHomogeneous(points)[:,0], T_mtx_T)[:, :3]
        pcd = open3d.PointCloud()
        pcd.points = open3d.Vector3dVector(points)
        pcd.colors = open3d.Vector3dVector(colors)

        # open3d.draw_geometries([pcd])
        open3d.write_point_cloud(baseReadPath + dataset + "/" + "Kinect2__" + captureFolder + ".ply", pcd)

        with open(baseReadPath + dataset + "/" + "Kinect2__" + captureFolder + ".bin", "wb") as fp:
            fp.write(struct.pack("i", len(pcd.points)))
            for pt in pcd.points:
                fp.write(
                    struct.pack("i", 3) + struct.pack("d", pt[0]) + struct.pack("d", pt[1]) + struct.pack("d", pt[2]))

        filterLocs = np.logical_and(np.logical_and(points[:, 2] < 950, points[:, 2] > 200),
                                    np.logical_and(np.logical_and(points[:, 0] < 530, points[:, 0] > -60),
                                                   np.logical_and(points[:, 1] < 160, points[:, 1] > -350)))
        points = points[filterLocs]
        colors = colors[filterLocs]
        pcd = open3d.PointCloud()
        pcd.points = open3d.Vector3dVector(points)
        pcd.colors = open3d.Vector3dVector(colors)

        open3d.write_point_cloud(baseReadPath + dataset + "/" + "filtered__Kinect2__" + captureFolder + ".ply", pcd)

        with open(baseReadPath + dataset + "/" + "filtered__Kinect2__" + captureFolder + ".bin", "wb") as fp:
            fp.write(struct.pack("i", len(pcd.points)))
            for pt in pcd.points:
                fp.write(
                    struct.pack("i", 3) + struct.pack("d", pt[0]) + struct.pack("d", pt[1]) + struct.pack("d", pt[2]))

# openni2.unload()
