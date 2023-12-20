#!/bin/bash

source ~/wali_desk/c3ws/install/local_setup.bash
export IGNITION_VERSION=fortress
echo -e "\n** LAUNCH IGNITION EMPTY WORLD **"
ros2 launch irobot_create_ignition_bringup create3_ignition.launch.py x:=1.0 y:=0.5 yaw:=1.5707

