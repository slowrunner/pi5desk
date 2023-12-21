#!/bin/bash

# REQ: apt-get install ros-<rosdistro>-teleop-twist-joy to install.


echo -e "\n*** Switching to ~/pi5desk/c3ws"
cd ~/pi5desk/c3ws

echo -e "\n*** Sourcing install/setup.bash"
. ~/pi5desk/c3ws//install/setup.bash

echo -e "\n*** Start SNES gamepad node"
echo '*** ros2 launch teleop_twist_joy teleop-launch.py joy_config:="snes_slow" '
ros2 launch teleop_twist_joy teleop-launch.py joy_config:="snes_slow" 

