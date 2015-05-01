# Raspberry Pi OpenCV-Python Face Recognition Lock

###Introduction
This project was part of the embedded system design course, and uses face recognition to control a servo lock. The face recognition has been done using the Eigenfaces algorithm (Principle Component Analysis or PCA) and implemented using the Python API of OpenCV. For more information about face recognition in OpenCV, see [Face Recognition with OpenCV](http://docs.opencv.org/modules/contrib/doc/facerec/facerec_tutorial.html).

###Motivation
It's a slight modification of the [Raspberry Pi Face Recognition Treasure Box](https://github.com/tdicola/pi-facerec-box) project by Tony Dicola on the [Adafruit Learning System](https://learn.adafruit.com/raspberry-pi-face-recognition-treasure-box/overview). The code has been modified at places to replace the use of the RPIO library (which has issues running on the new Raspberry Pi 2 Model B) with the standard RPi.GPIO library. The project has also been implemented to work as an automated home lock system which unlocks for the owner of the house and doesn't for any other visitor. It also plays an appropriate voice message.

###Software
The following is a copy of the Software installation procedure found in the original project documentation:

####OpenCV Installation
This project depends on the OpenCV computer vision library to perform the face detection and recognition. Unfortunately the current binary version of OpenCV available to install in the Raspbian operating system through apt-get (version 2.3.x) is too old to contain the face recognition algorithms used by this project. However you can download, compile, and install a later version of OpenCV to access the face recognition algorithms.
Note: Compiling OpenCV on the Raspberry Pi will take about 3 hours of mostly unattended time. Make sure you have some time to start the process before proceeding.

First you will need to install OpenCV dependencies before you can compile the code. Connect to your Raspberry Pi in a terminal session and execute the following command:
```
sudo apt-get update
sudo apt-get install build-essential cmake pkg-config python-dev libgtk2.0-dev libgtk2.0 zlib1g-dev libpng-dev libjpeg-dev libtiff-dev libjasper-dev libavcodec-dev swig unzip
```
Answer yes to any questions about proceeding and wait for the libraries and dependencies to be installed. You can ignore messages about packages which are already installed.
Next you should download and unpack the OpenCV source code by executing the following commands:
```
wget http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.10/opencv-2.4.10.zip
unzip opencv-2.4.10.zip
```
Note that this project was written using OpenCV 2.4.10, although any 2.4.x version of OpenCV should have the necessary face recognition algorithms.
Now change to the directory with the OpenCV source and execute the following cmake command to build the makefile for the project. Note that some of the parameters passed in to the cmake command will disable compiling performance tests and GPU accelerated algorithms in OpenCV. I found removing these from the OpenCV build was necessary to help reduce the compilation time, and successfully compile the project with the low memory available to the Raspberry Pi.
```
cd opencv-2.4.9
cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_PERF_TESTS=OFF -DBUILD_opencv_gpu=OFF -DBUILD_opencv_ocl=OFF
```
After this command executes you should see details about the build environment and finally a '-- Build files have been written to: ...' message. You might see a warning that the source directory is the same as the binary directory--this warning can be ignored (most cmake projects build inside a subdirectory of the source, but for some reason I couldn't get this to work with OpenCV and built it inside the source directory instead). If you see any other error or warning, make sure the dependencies above were installed and try executing the cmake command again.

Next, compile the project by executing:
```
make
```
This process will take a significant amount of time (about 3 hours), but you can leave it unattended as the code compiles.
Finally, once compilation is complete you can install the compiled OpenCV libraries by executing:
```
sudo make install
```
After this step the latest version of OpenCV should be installed on your Raspberry Pi.

####Python Dependencies
The code for this project is written in python and has a few dependencies that must be installed. Once connected to your Raspberry Pi in a terminal session, execute the following commands:
```
sudo apt-get install python-pip
sudo apt-get install python-dev
sudo pip install picamera
sudo pip install RPi.GPIO
```
You can ignore any messages about packages which are already installed or up to date. These commands will install the picamera library for access to the Raspberry Pi camera, and the GPIO library for access to the Pi GPIO pins and PWM support.

###Hardware
The Hardware required for this project are as follows:
1. Raspberry Pi ( I prefer Model 2 B)

2. Raspberry Pi Camera

3. Micro Servo

4. One Push Button

5. Power Supply for the Servo (5V Source)

6. One 10K resistor for pull down

7. Breadboard and Jumper wires for connections

The necessary circuit diagrams and further explanations are explained in depth in the original pdf accompanying the project. Kindly go through it first.
