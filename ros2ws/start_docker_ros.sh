#!/bin/bash

cd ~/pi5desk/ros2ws
docker run -it --net=host  -v ~/pi5desk/ros2ws:/ros2ws r2hdp
