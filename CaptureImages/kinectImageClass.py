from primesense import openni2
import numpy as np
from open3d import open3d
import cv2

class KinectImageClass:
    def __init__(self, open_ni_path="C:\Program Files\OpenNI2\Tools"):
        openni2.initialize(open_ni_path)

        self.dev = openni2.Device.open_any()

        self.depth_stream = self.dev.create_depth_stream()
        self.color_stream = self.dev.create_color_stream()
        self.depth_stream.start()
        self.color_stream.start()

    def capture_image(self, filename):
        frame_depth = self.depth_stream.read_frame()
        frame_color = self.color_stream.read_frame()
        self.convertImagesToPointCloud(frame_depth, frame_color, filename)

    def convertImagesToPointCloud(self, frame_depth, frame_color, filename):
        depth_img = np.array(frame_depth.get_buffer_as_uint16()).reshape(frame_depth.height, frame_depth.width)
        color_img = np.array(frame_color.get_buffer_as_triplet()).reshape(frame_color.height, frame_color.width, -1)

        cv2.imwrite(filename+"__Depth.tiff", depth_img)
        cv2.imwrite(filename+"__Depth.png", ((255*depth_img.astype(np.float64)-np.min(depth_img))/np.max(depth_img)).astype(np.uint8))
        cv2.imwrite(filename+"__rgb.png", color_img)

        #points = [[openni2.convert_depth_to_world(self.depth_stream, i, j, depth_img[j, i]) for i in range(640)]
        #          for j in range(480)]

        #color_inds = [[openni2.convert_depth_to_color(self.depth_stream, self.color_stream, i, j, depth_img[j, i])
        #               for i in range(640)] for j in range(480)]
        #points = np.array(points).reshape(-1, 3)
        #color_inds = np.clip(np.array(color_inds).reshape(-1, 2), [0, 0], [640 - 1, 480 - 1])
        #colors = (color_img[color_inds[:, 1], color_inds[:, 0]] / 255).astype(np.float32)

        #pcd = open3d.PointCloud()
        #pcd.points = open3d.Vector3dVector(points)
        #pcd.colors = open3d.Vector3dVector(colors)
        #open3d.write_point_cloud(filename+".ply", pcd)

    def unload(self):
        self.depth_stream.stop()
        self.color_stream.stop()
        openni2.unload()


