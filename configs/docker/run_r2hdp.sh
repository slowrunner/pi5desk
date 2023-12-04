#!/bin/bash

cd ~/pi5desk/ros2ws
# --rm    remove container after running
docker run -it --net=host  -v ~/pi5desk/ros2ws:/ros2ws -w /ros2ws --rm r2hdp
