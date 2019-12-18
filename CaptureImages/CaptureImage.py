import os
import cv2

GPHOTO_PATH = "gphoto2"
"""
########## Uncomment this block for a windows pc ######
os.environ["IOLIBS"] = r'/win32/iolibs'
os.environ["CAMLIBS"] = r'/win32/camlibs'

GPHOTO_PATH="D:/CameraLibs/win32/gphoto2.exe"
"""
TEMP_GPHOTO_DIR = "capture/out.temp"
GPHOTO_PARAMS = " --capture-image-and-download --filename "


def TakeImage():
    if os.path.isfile(TEMP_GPHOTO_DIR):
        os.remove(TEMP_GPHOTO_DIR)

    os.system(GPHOTO_PATH+GPHOTO_PARAMS+TEMP_GPHOTO_DIR)

    img = cv2.imread(TEMP_GPHOTO_DIR)

    os.remove(TEMP_GPHOTO_DIR)

    return img


def SaveImage(FileName):
    if os.path.isfile(FileName):
        os.remove(FileName)

    return os.system(GPHOTO_PATH + GPHOTO_PARAMS + FileName)

