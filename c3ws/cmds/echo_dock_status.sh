#!/bin/bash

echo -e "\n*** ECHO DOCK STATUS"
if [ $ROS_DISTRO == "galactic" ]
  then
    echo -e "ros2 topic echo /dock"
    ros2 topic echo /dock
  else
    echo -e "ros2 topic echo --once /dock_status"
    ros2 topic echo --once /dock_status
fi
