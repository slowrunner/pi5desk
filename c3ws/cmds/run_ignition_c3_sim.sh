#!/bin/bash

echo "Starting Create3 Sim in Ignition"
cd ~/wali_desk/c3ws
if [ -e install/local_setup.bash ]; then
  source install/local_setup.bash
fi

ros2 launch irobot_create_ignition_bringup create3_ignition.launch.py

# or with starting point
# ros2 launch irobot_create_ignition_bringup create3_ignition.launch.py x:=1.0 y:=0.5 yaw:=1.5707

# or with namespace
# ros2 launch irobot_create_ignition_bringup create3_ignition.launch.py namespace:=sim_wali
