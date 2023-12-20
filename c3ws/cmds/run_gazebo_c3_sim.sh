#!/bin/bash

echo "Starting Create3 Sim in Gazebo"
cd ~/wali_desk/c3ws
if [ -e install/setup.bash ]; then
  source install/setup.bash
fi

ros2 launch irobot_create_gazebo_bringup create3_gazebo.launch.py
