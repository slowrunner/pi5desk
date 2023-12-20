#/bin/bash

echo -e "\n*** ECHO ODOM"
if [ $ROS_DISTRO == "galactic" ]
  then
    echo -e "ros2 topic echo /odom"
    ros2 topic echo /odom
  else
    echo -e "ros2 topic echo --once --flow-style /odom"
    ros2 topic echo --once --flow-style -l 1 /odom
fi


