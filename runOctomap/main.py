import os
import subprocess

imgfmt = ".jpg"
baseReadPath = "../captures/"
datasets = ["Cup", "DragonParty", "Statue", "Punch", "ToyCar"]
base_output_path = "../out/octomap/"
octomap_exe_path = "../Octomap/x64/Debug/Octomap.exe"

for dataset in datasets:
    for captureFile in os.listdir(baseReadPath+dataset):
        file, ext = os.path.splitext(captureFile)
        if ext == ".bin" and file.startswith("filtered__"):
            ftp = baseReadPath+dataset+"/"+captureFile
            print("processing "+ftp)
            outpath = base_output_path+dataset+"/"
            os.makedirs(outpath, exist_ok=True)
            subprocess.call([octomap_exe_path, ftp, outpath+file+".bt"])