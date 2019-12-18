# Gray code structured light reconstruction

> Reconstructs a 3D scene with the use of a projector and a camera

This repo makes use of a projector and a camera to scan a scene and create a 3D model. To achieve this a structured light pattern is projected onto a scene. This is captured with a camera to determine dense correspondences. The repository also includes code which can be used in order to calibrate the camera-projector setup. The reconstruction code is based on ["Robust Pixel Classification for 3D Modeling with Structured Light"](https://www.cs.purdue.edu/cgvlab/papers/aliaga/gi07.pdf). Furthermore, the calibration code follows the technique detailed in: ["Simple, Accurate, and Robust Projector-Camera Calibration."](https://ieeexplore.ieee.org/document/6375029). For this, the direct and indirect light was calculated with the use of
 ["Fast Separation of Direct and Global Components of a Scene
using High-Frequency Illumination"](http://www.cs.columbia.edu/cg/pdfs/1156189195-Krishnan_TOG06.pdf). Rather than making use of the default checkerboard pattern for camera calibration, the ChArUco board from OpenCV was used as this is more robust.

![](docs/pngs/res.gif)

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Disclamer](#disclamer)
- [Citation](#cite)


---


## Installation

- Install python
- Install various depencancies such as numpy ( requirements.txt to come )
- Run the code

## Usage

1) Camera Calibration:
The CameraCalibration folder contains all the code for camera calibration
main.py uses the captured images in a directory to calibrate the projector-camera
GenerateAurcoAndChaurco.py will generate the calibration patterns used
The KinectCameraCalibration will calibrate each of the Kinect cameras seperatly
The KinectStereoCalibration can be used with a few sturdier images to calibrate the position of the RGB camera to the IR camera

2) Decode Gray Images:
This folder contains the code to decode the color patterns on all the images in a directory and outputs the binary, gray and invalid pixel map images 
The make file included in this directory can be used to make this project/rawpy/

3) Capture Images:
The CaptureImages directory contains all the code to capture the relivant images.
All the gray images can be produced with produceAllGrayImages
The crosshairs used to focus the camera to the center of the screen can be drawn with the DrawCorsshairs.py
The CaptureCode.py can be used to capture the gray images and decode them.
For this to work you will either need to chainge CaptureCode.py to work with opencv's capture image function or gPhoto2 will need to be setup correctly with your dslr camera
Furthermore, line 12: "GrayCodeConverterPath = "../DecodeGrayImages/DecodeGrayImages"" should be set to the correct path containing the executable of the graycode converter compiled in 2)
Please also ensure that the KinectImageClass is setup properly with your OpenNI environment so that it can take images with your Kinect
PS your Kinect should be plugged in, with the projector and the camera.

4) Reproject Images
Use the main.py to reproject the specified images, The main_less distortion reprojects the images using a differenct camera calibration matrix containing less distortion coeficients
The filter point cloud files were slow attemts to downsample the 3D scannes. This was replaced with the voxel downsampple
ReprojectAllKinect uses the OpenNI's version of reprojection, this is replaced by ReprojectAllKinectV2, which uses the obtained calibration for the Kinect

5) Octomap
In the runOctomap folder. The main.py needs setup with the relivant directories in the start of the file. It will then import the point clouds and create the relivant .bt files
Various other run scripts were placed in this foolder. These can be ignored

## Documentation

![](docs/pngs/report-05.png)
![](docs/pngs/report-06.png)
![](docs/pngs/report-07.png)
![](docs/pngs/report-08.png)
![](docs/pngs/report-09.png)
![](docs/pngs/report-10.png)
![](docs/pngs/report-11.png)
![](docs/pngs/report-12.png)
![](docs/pngs/report-13.png)
![](docs/pngs/report-14.png)
![](docs/pngs/report-15.png)
![](docs/pngs/report-16.png)
![](docs/pngs/report-17.png)
![](docs/pngs/report-18.png)
![](docs/pngs/report-19.png)
![](docs/pngs/report-20.png)
![](docs/pngs/report-21.png)
![](docs/pngs/report-22.png)
![](docs/pngs/report-23.png)
![](docs/pngs/report-24.png)
![](docs/pngs/report-25.png)
![](docs/pngs/report-26.png)
![](docs/pngs/report-27.png)
![](docs/pngs/report-28.png)
![](docs/pngs/report-29.png)
![](docs/pngs/report-30.png)
![](docs/pngs/report-31.png)
![](docs/pngs/report-32.png)
![](docs/pngs/report-33.png)
![](docs/pngs/report-34.png)
![](docs/pngs/report-35.png)
![](docs/pngs/report-36.png)
![](docs/pngs/report-37.png)
![](docs/pngs/report-38.png)
![](docs/pngs/report-39.png)
![](docs/pngs/report-40.png)

---

## Disclamer

This repository is for educational purposes only. The algorithms implemented here is my interpretation of the original authors' work. Due to this, they will most likely not produce the same results as the original implementations. All rights are reserved to the original authors of the papers this code was based on. 

## Citation

If you find this work useful, please ensure that you cite the origional authors:

	@inproceedings{3D-Modeling,
		author = {Xu, Yi and Aliaga, Daniel G.},
		title = {Robust Pixel Classification for 3D Modeling with Structured Light},
		booktitle = {Proceedings of Graphics Interface 2007},
		series = {GI '07},
		year = {2007},
		isbn = {978-1-56881-337-0},
		location = {Montreal, Canada},
		pages = {233--240},
		numpages = {8},
		acmid = {1268556},
		publisher = {ACM},
		address = {New York, NY, USA},
		keywords = {3D reconstruction, direct and global separation, structured light},
	} 

	@INPROCEEDINGS{calib, 
		author={D. Moreno and G. Taubin}, 
		booktitle={2012 Second International Conference on 3D Imaging, Modeling, Processing, Visualization Transmission}, 
		title={Simple, Accurate, and Robust Projector-Camera Calibration}, 
		year={2012}, 
		volume={}, 
		number={}, 
		pages={464-471}, 
		doi={10.1109/3DIMPVT.2012.77}, 
		ISSN={1550-6185}, 
		month={Oct},}

	@inproceedings{NayarSeperation,
		author = {Nayar, Shree K. and Krishnan, Gurunandan and Grossberg, Michael D. and Raskar, Ramesh},
		title = {Fast Separation of Direct and Global Components of a Scene Using High Frequency Illumination},
		booktitle = {ACM SIGGRAPH 2006 Papers},
		series = {SIGGRAPH '06},
		year = {2006},
		isbn = {1-59593-364-6},
		location = {Boston, Massachusetts},
		pages = {935--944},
		numpages = {10},
		acmid = {1141977},
		publisher = {ACM},
		address = {New York, NY, USA},
		keywords = {coded illumination, direct illumination, global illumination, image decomposition, image manipulation, interreflections, subsurface scattering, translucency, volumetric scattering},
	} 
