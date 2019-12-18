import os
import rawpy
import sys
import cv2
from subprocess import Popen

DETACHED_PROCESS = 0x00000008

saveDir = sys.argv[1]
imgFmt = sys.argv[2]

if imgFmt == ".cr2":
    print("Converting images in "+saveDir)

    for file in os.listdir(saveDir):
        print(file)
        f, ext = os.path.splitext(file)
        if ext == ".cr2":
            print("Converting: "+file)
            img = cv2.cvtColor(rawpy.imread(saveDir+file).postprocess(), cv2.COLOR_RGB2BGR)
            cv2.imwrite(saveDir+f+".tiff", img)
else:
    print("Skipping Conversion")

if len(sys.argv)>2 and sys.argv[3] is not None:
    print([sys.argv[3], saveDir, imgFmt])
    Popen([sys.argv[3] +" "+saveDir[:-1] +" "+ imgFmt if imgFmt != ".cr2" else ".tiff"], shell=True,
                    stdin=None, stdout=None,
                    stderr=None, close_fds=True)
cv2.waitKey(10000)
