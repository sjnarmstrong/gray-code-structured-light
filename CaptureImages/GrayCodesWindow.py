import cv2
from GrayImages import GrayImage
import numpy as np

gImg = GrayImage()
WINDOW_NAME = "GrayCodesWindow"


def getImageIteration(firstIteration=True, map1=None, map2=None):
    if firstIteration:
        print("First It")
        imgToDisplay = cv2.imread("InstructionImg.png", cv2.IMREAD_GRAYSCALE)
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.imshow(WINDOW_NAME, imgToDisplay)
        cv2.resizeWindow(WINDOW_NAME, imgToDisplay.shape[1], imgToDisplay.shape[0])
    else:
        print("Other Its")
        imgToDisplay = np.array([[0]], dtype=np.uint8)
        cv2.imshow(WINDOW_NAME, imgToDisplay)

    k = cv2.waitKey(0)

    if k != ord('\r'):
        return
    if firstIteration:
        cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);
    k = cv2.waitKey(2000)
    for imgnr, imgToDisplay in gImg.getIterator():
        print(imgnr)

        if map1 is not None and map2 is not None:
            imgToDisplay = cv2.remap(imgToDisplay, map1, map2, cv2.INTER_NEAREST)

        cv2.imshow(WINDOW_NAME, imgToDisplay)
        cv2.waitKey(10)
        yield imgnr

def destroyW():
    cv2.destroyWindow(WINDOW_NAME)
