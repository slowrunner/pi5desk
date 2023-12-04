#!/bin/bash

cd ~/pi5desk/ros2ws
# --rm remove container after exit
# --w workdir to start in
docker run -it --net=host  -v ~/pi5desk/ros2ws:/ros2ws --w /ros2ws --rm r2hd
echo -e "\n*** STARTING ROS 2 HUMBLE DESKTOP (osrf) IN DOCKER ***"
docker run -it --net=host  -v /home/pi:/home/pi -w /home/pi/pi5desk/ros2ws --rm r2hd
echo -e "\n*** EXITED DOCKER ***"
