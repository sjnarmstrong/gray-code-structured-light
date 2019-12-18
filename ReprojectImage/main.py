import cv2
import numpy as np
from open3d import open3d
import os
import struct

imgfmt = ".jpg"
baseReadPath = "../captures/"
datasets = ["Cup2", "Calib3", "Cup", "DragonParty", "Statue", "Punch", "ToyCar"]
CalibAtribs = np.load("../camera_calibration_out/calculated_cams_matrix.npz")
retval=CalibAtribs["retval"]
cameraMatrix1=CalibAtribs["cameraMatrix1"]
distCoeffs1=CalibAtribs["distCoeffs1"]
cameraMatrix2=CalibAtribs["cameraMatrix2"]
distCoeffs2=CalibAtribs["distCoeffs2"]
R=CalibAtribs["R"]
T=CalibAtribs["T"]
E=CalibAtribs["E"]
F=CalibAtribs["F"]
newcameramtx_camera=CalibAtribs["newcameramtx_camera"]
roi_camera=CalibAtribs["roi_camera"]
newcameramtx_proj=CalibAtribs["newcameramtx_proj"]
roi_proj=CalibAtribs["roi_proj"]
invCamMtx=CalibAtribs["invCamMtx"]
invProjMtx=CalibAtribs["invProjMtx"]

projector_resolution =(1024, 768)

T=T[:,0]
for dataset in datasets:
    for captureFolder in os.listdir(baseReadPath+dataset):
        if not os.path.isdir(baseReadPath+dataset+"/"+captureFolder):
            continue
        path = baseReadPath+dataset+"/"+captureFolder + "/"

        img = cv2.imread(path+"w.jpg")
        validV = cv2.imread(path + "out_InvalidImageV.tiff", cv2.IMREAD_GRAYSCALE)
        validH = cv2.imread(path + "out_InvalidImageH.tiff", cv2.IMREAD_GRAYSCALE)
        coordsV = cv2.imread(path + "out_BinImageH.tiff", cv2.IMREAD_ANYDEPTH + cv2.IMREAD_GRAYSCALE)
        coordsH = cv2.imread(path + "out_BinImageV.tiff", cv2.IMREAD_ANYDEPTH + cv2.IMREAD_GRAYSCALE)

        indImg1 = np.indices(coordsH.shape, coordsH.dtype)
        indImg1 = indImg1[:, np.logical_and(validV == 0, validH == 0)]

        colors = img[indImg1[0], indImg1[1]]

        indImg2 = np.vstack((coordsH[indImg1[0], indImg1[1]], coordsV[indImg1[0], indImg1[1]]))
        indImg1[[0, 1]] = indImg1[[1, 0]]
        indImg2[[0, 1]] = indImg2[[1, 0]]
        indImg1 = indImg1.T.astype(np.float64)
        indImg2 = indImg2.T.astype(np.float64)

        LPts = cv2.convertPointsToHomogeneous(cv2.undistortPoints(indImg1[None,], cameraMatrix1, distCoeffs1, R=R))[:,0].T
        RPts = cv2.convertPointsToHomogeneous(cv2.undistortPoints(indImg2[None,], cameraMatrix2, distCoeffs2))[:,0].T


        TLen = np.linalg.norm(T)
        NormedL = LPts/np.linalg.norm(LPts, axis=0)
        alpha = np.arccos(np.dot(-T, NormedL)/TLen)
        degalpha = alpha*180/np.pi
        beta = np.arccos(np.dot(T, RPts)/(TLen*np.linalg.norm(RPts, axis=0)))
        degbeta = beta*180/np.pi
        gamma = np.pi - alpha - beta
        P_len = TLen*np.sin(beta)/np.sin(gamma)
        Pts = NormedL*P_len

        colors[:,[0,2]]=colors[:,[2,0]]

        pcd = open3d.PointCloud()
        pcd.points = open3d.Vector3dVector(Pts.T)
        pcd.colors = open3d.Vector3dVector(colors.astype(np.float64)/255.0)
        open3d.write_point_cloud(baseReadPath+dataset+"/"+"capturedPointCloud_"+captureFolder + ".ply", pcd)

        with open(baseReadPath+dataset+"/"+"capturedPointCloud_"+captureFolder + ".bin", "wb") as fp:
            fp.write(struct.pack("i", len(Pts.T)))
            for pt in Pts.T:
                fp.write(struct.pack("i", 3)+struct.pack("d",pt[0])+struct.pack("d",pt[1])+struct.pack("d",pt[2]))

        downpcd = open3d.voxel_down_sample(pcd, voxel_size=0.5)
        #downpcd, ind = open3d.statistical_outlier_removal(downpcd,
        #                                             nb_neighbors=30, std_ratio=3)
        #downpcd = open3d.voxel_down_sample(cl, voxel_size=0.2)

        open3d.write_point_cloud(baseReadPath+dataset+"/"+"downsampled_capturedPointCloud_"+captureFolder + ".ply", downpcd)

        with open(baseReadPath+dataset+"/"+"downsampled_capturedPointCloud_"+captureFolder + ".bin", "wb") as fp:
            fp.write(struct.pack("i", len(downpcd.points)))
            for pt in downpcd.points:
                fp.write(struct.pack("i", 3)+struct.pack("d",pt[0])+struct.pack("d",pt[1])+struct.pack("d",pt[2]))


        pts_hold = np.array(downpcd.points)
        colors_hold = np.array(downpcd.colors)
        filterLocs = np.logical_and(np.logical_and(pts_hold[:, 2] < 950, pts_hold[:, 2] > 200),
                                    np.logical_and(np.logical_and(pts_hold[:, 0] < 530, pts_hold[:, 0] > -60),
                                                   np.logical_and(pts_hold[:, 1] < 160, pts_hold[:, 1] > -350)))
        pts_hold = pts_hold[filterLocs]
        colors_hold = colors_hold[filterLocs]
        pcd = open3d.PointCloud()
        pcd.points = open3d.Vector3dVector(pts_hold)
        pcd.colors = open3d.Vector3dVector(colors_hold)
        open3d.write_point_cloud(baseReadPath + dataset + "/" + "filtered__capturedPointCloud__" + captureFolder + ".ply", pcd)

        with open(baseReadPath + dataset + "/" + "filtered__capturedPointCloud__" + captureFolder + ".bin", "wb") as fp:
            fp.write(struct.pack("i", len(pcd.points)))
            for pt in pcd.points:
                fp.write(
                    struct.pack("i", 3) + struct.pack("d", pt[0]) + struct.pack("d", pt[1]) + struct.pack("d", pt[2]))
