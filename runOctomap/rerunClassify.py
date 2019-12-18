import os
import subprocess

imgfmt = ".jpg"
baseReadPath = "../captures/"
datasets = ["Cup2", "DragonParty2", "Statue2", "Punch2", "ToyCar2"]
base_output_path = "../out/octomap/"
classify_exe_path = "../DecodeGrayImages_old/x64/Debug/DecodeGrayImages.exe"

for dataset in datasets:
    for captureFolder in os.listdir(baseReadPath+dataset):
        ftp = baseReadPath+dataset+"/"+captureFolder
        if os.path.isdir(ftp):
            print("processing "+ftp)
            outpath = base_output_path+dataset+"/"
            os.makedirs(outpath, exist_ok=True)
            subprocess.call([classify_exe_path, "../captures/"+dataset+"/"+captureFolder])