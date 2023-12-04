#!/bin/bash


echo -e '\n*** Appending: export ROS_LOG_DIR="/home/pi/pi5desk/ros2ws/roslogs" to ~/.bashrc' 
echo 'export ROS_LOG_DIR="/home/pi/pi5desk/ros2ws/roslogs"' >> ~/.bashrc
echo -e '\n*** tail ~/.bashrc:'
tail ~/.bashrc
echo -e '\n'
