#!/bin/bash

cd ~/pi5desk/ros2ws
# --rm removes container after exit
docker run -it --net=host  -v ~/pi5desk/ros2ws:/ros2ws --rm r2hdp
