from primesense import openni2
import numpy as np
import cv2
openni2.initialize("C:\Program Files\OpenNI2\Tools")


dev = openni2.Device.open_any()

ir_stream = dev.create_ir_stream()
color_stream = dev.create_color_stream()

color_stream.set_video_mode(openni2.VideoMode(openni2.PIXEL_FORMAT_RGB888, 640, 480, 10))
ir_stream.set_video_mode(openni2.VideoMode(openni2.PIXEL_FORMAT_GRAY8, 640, 480, 5))
dev.set_depth_color_sync_enabled(True)

ir_stream.start()
color_stream.start()

captureNum = 0
k=None
while k != ord('q'):

    frame_color = color_stream.read_frame()
    frame_ir = ir_stream.read_frame()
    ir_img = np.array(frame_ir.get_buffer_as_uint8()).reshape(frame_ir.height, frame_ir.width)
    color_img = np.array(frame_color.get_buffer_as_triplet()).reshape(frame_color.height, frame_color.width, -1)
    cv2.imshow("depth",ir_img)
    cv2.imshow("color",color_img)
    k = cv2.waitKey(30)




ir_stream.stop()
color_stream.stop()
#openni2.unload()
