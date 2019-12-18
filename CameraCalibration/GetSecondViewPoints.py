import numpy as np
import cv2

def getCameraCoordinates(img, validV, validH, coordsV, coordsH, charucoCorners):

    charucoCorners[:, 0, [0, 1]] = charucoCorners[:, 0, [1, 0]]

    indices = np.indices((47, 47)).reshape(2, -1).T - 23

    new_points_camera = []
    new_points_projector = []
    valid_points = []

    for pt in charucoCorners:
        surroundingPoints = (np.rint(pt[:]) + indices).astype(np.int32)
        surroundingPoints = surroundingPoints[np.logical_and(np.logical_and(surroundingPoints[:, 0] < img.shape[0],
                                                                            surroundingPoints[:, 0] >= 0),
                                                             np.logical_and(surroundingPoints[:, 1] < img.shape[1],
                                                                            surroundingPoints[:, 1] >= 0))]
        isValid = np.logical_and(validV[surroundingPoints[:, 0], surroundingPoints[:, 1]] == 0,
                                 validH[surroundingPoints[:, 0], surroundingPoints[:, 1]] == 0)
        surroundingPoints = surroundingPoints[isValid]
        projector_points_u = coordsV[surroundingPoints[:, 0], surroundingPoints[:, 1]]
        projector_points_v = coordsH[surroundingPoints[:, 0], surroundingPoints[:, 1]]

        img[surroundingPoints[:, 0], surroundingPoints[:, 1]] = 255
        if len(projector_points_v)>0 and len(projector_points_u)>0:
            valid_points.append(True)
            projector_points = np.stack((projector_points_u, projector_points_v), axis=1)
            surroundingPoints[:,[0,1]]=surroundingPoints[:,[1,0]]
            H, mask = cv2.findHomography(surroundingPoints, projector_points, ransacReprojThreshold=2, maxIters=100000, method = cv2.FM_LMEDS, confidence=0.99)
            #print(H)
            #print(H is None)
            pt2 = np.dot(H, [pt[0,1], pt[0,0], 1.0])
            pt2 /= pt2[2]
            #print(pt2, coordsH[int(pt[0,0]), int(pt[0,1])], coordsV[int(pt[0,0]), int(pt[0,1])] )
            new_points_camera.append([[pt[0,1], pt[0,0]]])
            new_points_projector.append([[pt2[0], pt2[1]]])
        else:
            valid_points.append(False)
    return valid_points, np.array(new_points_camera, dtype=np.float32), np.array(new_points_projector, dtype=np.float32)


