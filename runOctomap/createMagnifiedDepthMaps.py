import os
import cv2
import numpy as np

imgfmt = ".jpg"
baseReadPath = "../captures/"
datasets = ["Cup", "DragonParty", "Statue", "Punch", "ToyCar", "Cup2", "DragonParty2", "Statue2", "Punch2", "ToyCar2"]
base_output_path = "../out/octomap/"
classify_exe_path = "../DecodeGrayImages_old/x64/Debug/DecodeGrayImages.exe"

for dataset in datasets:
    for captureFolder in os.listdir(baseReadPath+dataset):
        ftp = baseReadPath+dataset+"/"+captureFolder+"/"
        if os.path.isdir(ftp):
            print("processing "+ftp)
            img = cv2.imread(ftp+"out_GrayImageH.tiff", cv2.IMREAD_ANYDEPTH+cv2.IMREAD_GRAYSCALE)
            invalidH = cv2.imread(ftp + "out_InvalidImageH.tiff", cv2.IMREAD_GRAYSCALE)>0

            for bit_number in range(10):
                masked_img = ((img >> bit_number) & 1).astype(np.uint8)*255
                masked_img = cv2.cvtColor(masked_img, cv2.COLOR_GRAY2BGR)
                masked_img[invalidH] = (34, 0, 227)
                cv2.imwrite(ftp+"masked_out_"+str(bit_number)+"_grayImageH.png", masked_img)

            img = cv2.imread(ftp+"out_BinImageH.tiff", cv2.IMREAD_ANYDEPTH+cv2.IMREAD_GRAYSCALE)

            mC = np.min(img)
            rC = float(np.max(img)-mC)
            img = 255*(img.astype(np.float32)-mC)/rC
            cv2.imwrite(ftp+"scaled_out_BinImageH.png", img.astype(np.uint8))

            img = cv2.imread(ftp+"out_GrayImageV.tiff", cv2.IMREAD_ANYDEPTH+cv2.IMREAD_GRAYSCALE)
            invalidH = cv2.imread(ftp + "out_InvalidImageV.tiff", cv2.IMREAD_GRAYSCALE)>0

            for bit_number in range(10):
                masked_img = ((img >> bit_number) & 1).astype(np.uint8)*255
                masked_img = cv2.cvtColor(masked_img, cv2.COLOR_GRAY2BGR)
                masked_img[invalidH] = (34, 0, 227)
                cv2.imwrite(ftp+"masked_out_"+str(bit_number)+"_GrayImageV.png", masked_img)

            img = cv2.imread(ftp+"out_BinImageV.tiff", cv2.IMREAD_ANYDEPTH+cv2.IMREAD_GRAYSCALE)
            mC = np.min(img)
            rC = float(np.max(img)-mC)
            img = 255*(img.astype(np.float32)-mC)/rC
            cv2.imwrite(ftp+"scaled_out_BinImageV.png", img.astype(np.uint8))

            #validV = cv2.imread(path + "out_InvalidImageV.tiff", cv2.IMREAD_GRAYSCALE)
