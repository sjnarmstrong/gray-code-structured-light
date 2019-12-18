import cv2
import numpy as np

img = cv2.imread("../captures/c_1/w.jpg")

CalibAtribs = np.load("../camera_calibration_out/calculated_cams_matrix.npz")
retval=CalibAtribs["retval"]
cameraMatrix1=CalibAtribs["cameraMatrix1"]
distCoeffs1=CalibAtribs["distCoeffs1"]
cameraMatrix2=CalibAtribs["cameraMatrix2"]
distCoeffs2=CalibAtribs["distCoeffs2"]
R=CalibAtribs["R"]
T=CalibAtribs["T"]
E=CalibAtribs["E"]
F=CalibAtribs["F"]
newcameramtx_camera=CalibAtribs["newcameramtx_camera"]
roi_camera=CalibAtribs["roi_camera"]
newcameramtx_proj=CalibAtribs["newcameramtx_proj"]
roi_proj=CalibAtribs["roi_proj"]
invCamMtx=CalibAtribs["invCamMtx"]
invProjMtx=CalibAtribs["invProjMtx"]

ret = cv2.undistort(img, cameraMatrix1, distCoeffs1, newCameraMatrix=newcameramtx_camera)
cv2.namedWindow("undestort", cv2.WINDOW_NORMAL)
cv2.imshow("undestort", ret)
cv2.namedWindow("orig", cv2.WINDOW_NORMAL)
cv2.imshow("orig", img)
cv2.imwrite("Undistorted.png", ret)
cv2.waitKey(0)
cv2.destroyAllWindows()
