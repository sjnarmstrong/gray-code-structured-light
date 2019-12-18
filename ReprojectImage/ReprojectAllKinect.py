from primesense import openni2
import numpy as np
from open3d import open3d
import os
import cv2
import struct

imgfmt = ".jpg"
baseReadPath = "../captures/"
datasets = ["Cup", "DragonParty", "Statue", "Punch", "ToyCar"]
open_ni_path="C:\Program Files\OpenNI2\Tools"
openni2.initialize(open_ni_path)

dev = openni2.Device.open_any()

depth_stream = dev.create_depth_stream()
color_stream = dev.create_color_stream()
for dataset in datasets:
    for captureFolder in os.listdir(baseReadPath+dataset):
        if not os.path.isdir(baseReadPath+dataset+"/"+captureFolder):
            continue
        path = baseReadPath+dataset+"/"+captureFolder + "/"
        depth_img = cv2.imread(path + "kinect___Depth.tiff", cv2.IMREAD_GRAYSCALE+cv2.IMREAD_ANYDEPTH)
        color_img = cv2.imread(path + "kinect___rgb.png").astype(np.float64)
        color_img /= color_img.max(axis=(0,1))
        points = [[openni2.convert_depth_to_world(depth_stream, i, j, depth_img[j, i]) for i in range(640)]
                  for j in range(480)]

        color_inds = [[openni2.convert_depth_to_color(depth_stream, color_stream, i, j, depth_img[j, i])
                       for i in range(640)] for j in range(480)]
        points = np.array(points).reshape(-1, 3)*[1,1,-1]
        color_inds = np.clip(np.array(color_inds).reshape(-1, 2), [0, 0], [640 - 1, 480 - 1])
        colors = color_img[color_inds[:, 1], color_inds[:, 0]]

        pcd = open3d.PointCloud()
        pcd.points = open3d.Vector3dVector(points)
        pcd.colors = open3d.Vector3dVector(colors)
        open3d.write_point_cloud(baseReadPath+dataset+"/"+"Kinect__"+captureFolder+".ply", pcd)

        with open(baseReadPath+dataset+"/"+"Kinect__"+captureFolder + ".bin", "wb") as fp:
            fp.write(struct.pack("i", len(pcd.points)))
            for pt in pcd.points:
                fp.write(struct.pack("i", 3)+struct.pack("d",pt[0])+struct.pack("d",pt[1])+struct.pack("d",pt[2]))

openni2.unload()

