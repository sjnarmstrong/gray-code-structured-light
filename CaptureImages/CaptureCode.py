from GrayCodesWindow import getImageIteration, destroyW
from CaptureImage import SaveImage
import os
from subprocess import Popen
import cv2
from kinectImageClass import KinectImageClass
kic = KinectImageClass("/opt/OpenNI2/Bin/x64-Release")

DETACHED_PROCESS = 0x00000008 
BaseOutputDirBeforeNew = "../captures/"
SubCaptDir = "c_"
SaveFormat = ".jpg"

GrayCodeConverterPath = "../DecodeGrayImages/DecodeGrayImages"

cFolder = input("Enter capture folder: ")
BaseOutputDir = BaseOutputDirBeforeNew +cFolder+"/"

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
    for imgnr in getImageIteration(FirstIteration):
        if imgnr == "w":
            kic.capture_image(CamDirOut+"kinect_")
        SaveImage(CamDirOut+imgnr+SaveFormat)

        DoNextIteration=True
    if DoNextIteration:
        Popen(["python3 ConvertRawImage.py "+CamDirOut +" "+ SaveFormat +" "+ GrayCodeConverterPath], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    FirstIteration=False
destroyW()
kic.unload()
