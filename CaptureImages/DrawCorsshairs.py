import cv2
import numpy as np

img = np.zeros((768, 1024), dtype = np.uint8)
WINDOW_NAME="crosshairs"

img[768//2, 1024//2-20:1024//2+20] = 255
img[768//2+1, 1024//2-20:1024//2+20] = 255
img[768//2-20:768//2+20, 1024//2] = 255
img[768//2-20:768//2+20, 1024//2+1] = 255

img[768//2, 1024//2-20+150:1024//2+20-150] = 255
img[768//2+1, 1024//2-20+150:1024//2+20-150] = 255
img[768//2-20:768//2+20, 1024//2-150] = 255
img[768//2-20:768//2+20, 1024//2-151] = 255

imgToDisplay = cv2.imread("InstructionImg.png", cv2.IMREAD_GRAYSCALE)
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.imshow(WINDOW_NAME, imgToDisplay)
cv2.resizeWindow(WINDOW_NAME, imgToDisplay.shape[1], imgToDisplay.shape[0])
k = cv2.waitKey(0)
cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);
cv2.imshow(WINDOW_NAME, img)
cv2.waitKey(0)
cv2.destroyAllWindows()

