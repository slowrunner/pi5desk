#!/bin/bash

echo -e "\n*** STARTING ROS2 SLAM-TOOLBOX LOCALIZATION"
ros2 launch slam_toolbox localization_launch.py 'slam_params_file:=./my_loc_params.yaml'

