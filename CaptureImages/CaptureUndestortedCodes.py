from GrayCodesWindow import getImageIteration, destroyW
from CaptureImage import SaveImage
import os
from subprocess import Popen
import cv2
import numpy as np
from GrayImages import GrayImage

calib = np.load("../camera_calibration_out/calculated_cams_matrix.npz")

cameraMatrix = calib['cameraMatrix2']
distCoeffs = calib['distCoeffs2']
R = calib['R2']
newCameraMatrix = calib['P2']
gi = GrayImage()
map1, map2 = cv2.initUndistortRectifyMap(cameraMatrix, distCoeffs, np.eye(3), cameraMatrix, (gi.width, gi.height), cv2.CV_16SC2)


DETACHED_PROCESS = 0x00000008
BaseOutputDir = "../captures/"
SubCaptDir = "c_"
SaveFormat = ".jpg"

GrayCodeConverterPath = "../DecodeGrayImages/DecodeGrayImages"

currentI = -1
if os.path.isdir(BaseOutputDir):
    print("isdir")
    for folder in os.listdir(BaseOutputDir):
        print(folder)
        if os.path.isdir(BaseOutputDir+folder) and folder.startswith(SubCaptDir):
            try:
                currentI = max(currentI, int(folder[len(SubCaptDir):]))
            except:
                pass
DoNextIteration = True
FirstIteration = True
while DoNextIteration:
    currentI += 1
    DoNextIteration = False
    CamDirOut = BaseOutputDir+SubCaptDir+str(currentI)+"/"
    for imgnr in getImageIteration(FirstIteration, map1, map2):
        SaveImage(CamDirOut+imgnr+SaveFormat)
        cv2.waitKey(1000)
        DoNextIteration=True
    if DoNextIteration:
        Popen(["python3 ConvertRawImage.py "+CamDirOut +" "+ SaveFormat +" "+ GrayCodeConverterPath], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    FirstIteration=False
destroyW()
