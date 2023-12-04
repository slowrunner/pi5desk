#!/bin/bash

cd ~/pi5desk/ros2ws
# --rm  remove containter after finished
docker run -it --net=host  -v ~/pi5desk/ros2ws:/ros2ws -w /ros2ws --rm r2hd
