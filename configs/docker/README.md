# Install ROS 2 Humble To Pi5 PiOS Bookworm In Docker

REF: https://docs.ros.org/en/humble/How-To-Guides/Installing-on-Raspberry-Pi.html#raspberry-pi-os-with-ros-2-in-docker

** install Docker
- 1_setup_docker_apt_repo.sh  
- 2__install_docker_pkgs.sh   

Hello from Docker!  
This message shows that your installation appears to be working correctly.  

To generate this message, Docker took the following steps:  
 1. The Docker client contacted the Docker daemon.  
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.  
    (arm64v8)  
 3. The Docker daemon created a new container from that image which runs the  
    executable that produces the output you are currently reading.  
 4. The Docker daemon streamed that output to the Docker client, which sent it  
    to your terminal.  


- 3_clone_ros_docker_images.sh  
- 4_build_humble_desktop_container.sh  

- 5_test_ros_docker.md  (reproduced here)  

test: docker run hello-world  

# Create ros2ws/src directory  
mkdir -p ~/pi5desk/c3ws/src  
cd ~/pi5desk/c3ws

# start Docker mounting ros2ws  
docker run -it -v ~/pi5desk/c3ws:/c3ws r2hd  

   cd /c3ws  
   ros2 pkg list  
   ros2 run demo_nodes_cpp listener & ros2 run demo_nodes_cpp talker  
   cntrl-c  
   ps -ef | grep ros  
   kill x y  
   exit  


- 6_build_humble_desktop_plus_container.sh  

This add all the packages and configuration needed specifically for Wali

Run with:  ./run_docker_r2hdp.sh  

```
docker run -it --net=host  -v /home/pi:/home/pi -v /dev/input:/dev/input \
 -v /dev/bus/usb:/dev/bus/usb  -w /home/pi/pi5desk/c3ws --privileged --rm r2hdp
```



## CLEAN UP AFTER A REBUILD  

```
 $ docker image list  
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE  
r2hdp        latest    a32732c7e869   2 hours ago   3.41GB  
<none>       <none>    beceb7b58a39   2 days ago    3.37GB  
r2hd         latest    20eb98163bc8   2 days ago    3.23GB  


pi@RPi5DESK:~/pi5desk/configs/docker $ docker image rm beceb7b58a39  
Error response from daemon: conflict: unable to delete beceb7b58a39 (must be forced) - image is being used by stopped container 9b9ae547247a  

pi@RPi5DESK:~/pi5desk/configs/docker $ docker container list -a  
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES  
9b9ae547247a   r2hdp    ...  

pi@RPi5DESK:~/pi5desk/configs/docker $ docker image rm -f beceb7b58a39  
Deleted: sha256:beceb7b58a39f7cd26fd32bbbc222d7fe9b591682a40a07ff9bef9be426d92d0  

# or use docker container prune to remove all stopped containers  
pi@RPi5DESK:~/pi5desk/configs/docker $ docker container rm -f 9b9ae547247a  
9b9ae547247a  

pi@RPi5DESK:~/pi5desk/configs/docker $ docker image list  
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE  
r2hdp        latest    a32732c7e869   2 hours ago   3.41GB  
r2hd         latest    20eb98163bc8   2 days ago    3.23GB  


```


## Joystick access from Docker  

- Required apt packages  ```RUN apt install -y xxx yyy```  
  - joystick  
  - python3-pip  

- Since running on PiOS, evdev will need /home/pi/ to exist  
  - ```RUN useradd -s /bin/bash pi``` will create /home/pi/  

- Required python packages  
  - evdev  ```RUN sudo pip3 install evdev```  

- Copy gamepad config file into container  

```
# files to copy must be in the docker tree
COPY snes_slow.config.yaml /opt/ros/humble/share/teleop_twist_joy/config/
```

- Run in --privileged mode  

```
docker run -it --net=host  -v /home/pi:/home/pi -v /dev/input:/dev/input \
 -v /dev/bus/usb:/dev/bus/usb  -w /home/pi/pi5desk/c3ws --privileged --rm r2hdp
```
