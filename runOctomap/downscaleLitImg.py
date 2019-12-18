import cv2
import os


imgfmt = ".jpg"
baseReadPath = "../captures/"
datasets = ["Cup", "DragonParty", "Statue", "Punch", "ToyCar", "Cup2", "DragonParty2", "Statue2", "Punch2", "ToyCar2"]
base_output_path = "../out/octomap/"
classify_exe_path = "../DecodeGrayImages_old/x64/Debug/DecodeGrayImages.exe"
dwidth = 640.0
for dataset in datasets:
    for captureFolder in os.listdir(baseReadPath+dataset):
        ftp = baseReadPath+dataset+"/"+captureFolder+"/"
        if os.path.isdir(ftp):
            print("processing "+ftp)
            img = cv2.imread(ftp+"w.jpg")
            if img is None:
                print("skipping "+ftp)
                continue
            imgwidth = img.shape[1]
            scale = dwidth/imgwidth
            img = cv2.resize(img, None, fx=scale, fy=scale)
            cv2.imwrite(ftp+"w_rescaled.jpg", img)