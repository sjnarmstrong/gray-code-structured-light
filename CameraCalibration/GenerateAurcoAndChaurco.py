import cv2
import numpy as np
from cv2 import aruco
import BoardInfo

aw=BoardInfo.blocksx*BoardInfo.desired_block_size_mm
ah=BoardInfo.blocksy*BoardInfo.desired_block_size_mm
img = BoardInfo.charucoBoard.draw((aw*BoardInfo.dpmm, ah*BoardInfo.dpmm))
cv2.imwrite("charucoBoard.png", img)

aw2=BoardInfo.blocksx2*BoardInfo.desired_block_size_mm+(BoardInfo.blocksx2-1)*BoardInfo.desired_gap_size_mm
ah2=BoardInfo.blocksy2*BoardInfo.desired_block_size_mm+(BoardInfo.blocksy2-1)*BoardInfo.desired_gap_size_mm
img = BoardInfo.arucoBoard.draw((aw2*BoardInfo.dpmm, ah2*BoardInfo.dpmm))
cv2.imwrite("arucoBoard.png", img)

