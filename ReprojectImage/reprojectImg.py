import cv2
import numpy as np
from open3d import open3d

image_nr=43
#image_nr=28
basePath = """../captures/Statue/c_0/"""
imgfmt = ".jpg"
projector_resolution =(1024, 768)
path = basePath.format(image_nr)

img = cv2.imread(basePath+"w.jpg")
validV = cv2.imread(path + "out_InvalidImageV.tiff", cv2.IMREAD_GRAYSCALE)
validH = cv2.imread(path + "out_InvalidImageH.tiff", cv2.IMREAD_GRAYSCALE)
coordsV = cv2.imread(path + "out_BinImageH.tiff", cv2.IMREAD_ANYDEPTH + cv2.IMREAD_GRAYSCALE)
coordsH = cv2.imread(path + "out_BinImageV.tiff", cv2.IMREAD_ANYDEPTH + cv2.IMREAD_GRAYSCALE)

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
T=T[:,0]

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
#np.savez("saved_point_could_data.npz", Pts, indImg1)
pcd = open3d.PointCloud()
pcd.points = open3d.Vector3dVector(Pts.T)
pcd.colors = open3d.Vector3dVector(colors.astype(np.float64)/255.0)

#downpcd = open3d.voxel_down_sample(pcd, voxel_size = 0.10)

#open3d.draw_geometries([downpcd])

downpcd = open3d.voxel_down_sample(pcd, voxel_size=0.5)
#cl,ind = open3d.statistical_outlier_removal(downpcd,
#            nb_neighbors=30, std_ratio=3)

points = np.array(downpcd.points)
filterLocs = np.logical_and(np.logical_and(points[:, 2] < 950, points[:, 2] > 200),
                            np.logical_and(np.logical_and(points[:, 0] < 530, points[:, 0] > -60),
                                           np.logical_and(points[:, 1] < 160, points[:, 1] > -350)))

pcd = open3d.PointCloud()
pcd.points = open3d.Vector3dVector(points[filterLocs])
pcd.colors = open3d.Vector3dVector(np.array(downpcd.colors)[filterLocs])
#downpcd = open3d.voxel_down_sample(cl, voxel_size = 0.5)
open3d.draw_geometries([pcd])

#pcd2 = open3d.PointCloud()
#pcd2.points = open3d.Vector3dVector((Pts+[100,0,0]).T)
#open3d.draw_geometries([pcd, pcd2])


###Start filter points

