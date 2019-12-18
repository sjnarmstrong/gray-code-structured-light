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

pc_mag = np.linalg.norm(pointcloud, axis=0)

CalibAtribs = np.load("../camera_calibration_out/calculated_cams_matrix.npz")
cameraMatrix1=CalibAtribs["cameraMatrix1"]
distCoeffs1=CalibAtribs["distCoeffs1"]
R=CalibAtribs["R"]

min = np.min(image_coords, axis=0)
max = np.max(image_coords, axis=0)
range = max-min
step = range/desigred_cloud_dims
new_x_coords = (np.arange(0, desigred_cloud_dims[0], 1)+0.5)*step[0]+min[0]
new_y_coords = (np.arange(0, desigred_cloud_dims[1], 1)+0.5)*step[1]+min[1]


img_coords = np.stack(np.meshgrid(new_x_coords, new_y_coords), axis=2).reshape(-1, 2)
img_int_coords = np.rint(img_coords).astype(np.int32)
colors = img[img_int_coords[:, 1], img_int_coords[:, 0]]


new_L_pts = cv2.undistortPoints(img_coords[None,], cameraMatrix1, distCoeffs1, R=R)[0]
old_L_pts = (pointcloud[0:2]/pointcloud[2]).T

new_point_cloud = cv2.convertPointsToHomogeneous(new_L_pts.copy())[:, 0]
new_point_cloud /= np.linalg.norm(new_point_cloud, axis=1)[:, None]
#new_point_cloud = new_point_cloud.reshape(desigred_cloud_dims[0], desigred_cloud_dims[1], 3)

#new_L_pts = new_L_pts.reshape(desigred_cloud_dims[0], desigred_cloud_dims[1], 2)
#pt_row = new_L_pts[0]

for i, pt in enumerate(new_L_pts):
    #normT_2 = (pt_row[:, None] - old_L_pts[None]) ** 2
    #normT_2 = normT_2[:,:,0] - normT_2[:,:,1]
    #nearist_n = np.argpartition(normT_2, 4, axis=1)[:, :4]
    #new_point_cloud[i] *= np.average(pc_mag[nearist_n], axis=1)[:, None]
    nearist_n = np.argpartition(np.linalg.norm(pt - old_L_pts, axis=1), 4, axis=0)[:4]
    new_point_cloud[i] *= np.average(pc_mag[nearist_n])
    print(i/len(new_L_pts)*100)

pcd = open3d.PointCloud()
pcd.points = open3d.Vector3dVector(new_point_cloud)
pcd.colors = open3d.Vector3dVector(colors.astype(np.float64)/255.0)
open3d.draw_geometries([pcd])
