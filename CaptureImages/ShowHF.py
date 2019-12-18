import cv2
from GrayImages import BinaryImage


gImg = BinaryImage()
WINDOW_NAME = "GrayCodesWindow"

imgToDisplay = cv2.imread("InstructionImg.png", cv2.IMREAD_GRAYSCALE)

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.imshow(WINDOW_NAME, imgToDisplay)
cv2.resizeWindow(WINDOW_NAME, imgToDisplay.shape[1], imgToDisplay.shape[0])
k = cv2.waitKey(0)


cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
imgToDisplay = gImg.getImage(gImg.num_bits-1 )
cv2.imshow(WINDOW_NAME, imgToDisplay)
cv2.waitKey(0)


cv2.destroyWindow(WINDOW_NAME)