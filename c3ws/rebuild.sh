#/bin/bash

echo -e "\n** SOURCE .bashrc"
. ~/.bashrc

echo -e "** CHANGE to wali_desk/c3ws"
cd ~/wali_desk/c3ws

echo -e "** INSTALL ANY ROS DEPENDENCIES **"
rosdep install -i --from-path src

echo -e "** COLCON BUILD w/SYMLINK-INSTALL"
colcon build --symlink-install

echo -e "** SOURCE BUILT SETUP.BASH"
. install/setup.bash
