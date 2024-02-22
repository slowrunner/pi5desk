# RGB Tiny YOLO v4 with Spatial Data (with and without visual display)

CODE: https://raw.githubusercontent.com/luxonis/depthai-python/main/examples/SpatialDetection/spatial_tiny_yolo.py  
BLOB: https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/yolo-v4-tiny-tf_openvino_2021.4_6shave.blob  

REF: https://docs.luxonis.com/projects/api/en/latest/samples/SpatialDetection/spatial_tiny_yolo/  


```
mkdir ../models
wget https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/yolo-v4-tiny-tf_openvino_2021.4_6shave.blob
cp *.blob ../models
wget https://raw.githubusercontent.com/luxonis/depthai-python/main/examples/SpatialDetection/spatial_tiny_yolo.py
cp spatial_tiny_yolo.py orig_spatial_tiny_yolo.py
python3 orig_spatial_tiny_yolo.py


== Modified with image and depth display option

./spatial_tiny_yolo.py [-d] [--display] [-h] [--help]
optional arguments:
  -h, --help     show this help message and exit
  -d, --display  display annotated rgb images and depth map

== Modified for results only, no image display

./console_spatial_tiny_yolo.py  

```

Spatial Tiny-yolo (with optional image, objects, and depth display)  
  Performs inference on RGB camera and retrieves spatial location coordinates: x (h), y (v), z (range) relative to device  
  Using  tiny-yolo-v4 network on rgb camerafor object recognition and stereo depth network on left+right greyscale cameras 

# ANALYSIS (Raspberry Pi 3B+ Legacy Pi OS 2021-12):

 - Base: Ave load 0.02 (0.2 w/VNC desktop) 41degC 5.8 Watts 0.49A at 11.8V

 - Returning rgb preview annotated with object boundary and spacial x,y,z data, and full depthmap display  
   13-19 FPS Ave RPi3B+ load 4.0 (peak 5.5) Temp: 65degC (no throttling, soft temp limit 0x8 flag set)  
   (displayed on remote desktop via VNC)  
   12.4 Watts (1.2A at 10.4V)  
   ~ 6.6 Watts for Oak-D-Lite and display load  
   ~ 4.0 ave load - 100% of four cores at maximum processor frequency  
   ~ 18degC processor temperature load (unaspirated heatsink)  

```
 10:44:56 up 55 min,  3 users,  load average: 5.48, 4.89, 2.78
temp=65.5'C
frequency(48)=1200000000
throttled=0x80008

NN fps: 13.9     
chair      X:107    Y:315    Z:2732  mm
 
NN fps: 13.9     
chair      X:100    Y:287    Z:2707  mm
 
NN fps: 16.0     
chair      X:117    Y:304    Z:2690  mm
 
NN fps: 16.0     
chair      X:112    Y:301    Z:2717  mm

```

![Spatial_Tiny_Yolo on RPi3B+](Oak-D-Lite_Spatial_Tiny_Yolo_RPi3Bplus.jpg?raw=true)



 - Returning console only YoloSpatialDetection label with x,y,z data  
   27-30 FPS Ave RPi3B+ load 0.25 Temp: 43degC (no throttling, no flags)  
   10.4 Watts (0.93A at 11.1V)  
   ~ 4.6 Watts for Oak-D-Lite operation  
   ~ 0.2 ave load 20% of one-of-four cores at minimum processor frequency (~2% of processor)  
   ~ 2degC processor temperature load     
   

```
 10:34:22 up 45 min,  3 users,  load average: 0.24, 0.23, 0.16
temp=45.6'C
frequency(48)=700000000
throttled=0x0



NN fps: 30.0     
chair      X:118    Y:261    Z:2701  mm

person     X:-821   Y:394    Z:2846  mm
 
NN fps: 30.0     
chair      X:119    Y:276    Z:2717  mm

person     X:-824   Y:382    Z:2856  mm
 
NN fps: 30.0     
chair      X:121    Y:274    Z:2768  mm
 
NN fps: 30.0     
chair      X:119    Y:277    Z:2728  mm

person     X:-829   Y:398    Z:2873  mm
 
NN fps: 30.0     
chair      X:138    Y:264    Z:2730  mm
```


```
pi@PIOSLGCY:~/GoPiLgc $ cat /etc/os-release 
PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"

pi@PIOSLGCY:~/GoPiLgc $ uname -a
Linux PIOSLGCY 5.10.63-v7+ #1496 SMP Wed Dec 1 15:58:11 GMT 2021 armv7l GNU/Linux
```
