import cv2
import numpy as np
from open3d import open3d

image_nr=43
#image_nr=28
desigred_cloud_dims = np.array([640, 480])
imgfmt = ".jpg"

img = cv2.imread("../captures/c_"+str(image_nr)+"/w.jpg")

dta = np.load("saved_point_could_data.npz")
pointcloud, image_coords = dta['arr_0'], dta['arr_1']

CalibAtribs = np.load("../camera_calibration_out/calculated_cams_matrix.npz")
cameraMatrix1=CalibAtribs["cameraMatrix1"]
distCoeffs1=CalibAtribs["distCoeffs1"]
R=CalibAtribs["R"]

dists = np.linalg.norm(pointcloud, axis=0)
image_coords = image_coords.astype(np.int32)

depth_image = np.empty(img.shape[:-1], np.float32)
depth_image[:, :] = float('nan')
depth_image[image_coords[:,1], image_coords[:,0]] = dists


mask= np.indices((11, 11)) - 5
mask = np.exp(-(mask[0]**2+mask[1]**2)/(2*2.0*2.0))
mask *= 11*11/np.sum(mask)


min = np.min(image_coords, axis=0)
max = np.max(image_coords, axis=0)
range = max-min
step = range/desigred_cloud_dims
new_x_coords = (np.arange(0, desigred_cloud_dims[0], 1)+0.5)*step[0]+min[0]
new_y_coords = (np.arange(0, desigred_cloud_dims[1], 1)+0.5)*step[1]+min[1]

new_img_coords = np.stack(np.meshgrid(new_x_coords, new_y_coords), axis=2).reshape(-1, 2)
avg_depth = np.empty(new_img_coords.shape[0], np.float64)

for i, pt in enumerate(new_img_coords):
    ipt = np.rint(pt).astype(np.int32)
    pt_depth = np.nanmean(np.multiply(depth_image[ipt[1]-5:ipt[1]+6, ipt[0]-5:ipt[0]+6], mask))
    avg_depth[i] = pt_depth

LPtsNew = cv2.convertPointsToHomogeneous(cv2.undistortPoints(new_img_coords[None,], cameraMatrix1, distCoeffs1, R=R))[:,0].T
LPtsNew /= np.linalg.norm(LPtsNew, axis=0)
LPtsNew *= avg_depth

img_int_coords = np.rint(new_img_coords).astype(np.int32)
colors = img[img_int_coords[:, 1], img_int_coords[:, 0]]

pcd = open3d.PointCloud()
pcd.points = open3d.Vector3dVector(LPtsNew.T)
pcd.colors = open3d.Vector3dVector(colors.astype(np.float64)/255.0)
open3d.draw_geometries([pcd])