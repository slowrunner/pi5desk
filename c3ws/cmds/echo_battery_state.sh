#/bin/bash

echo -e "\n*** ECHO BATTERY STATE"
if [ $ROS_DISTRO == "galactic" ]
  then
    echo -e "ros2 topic echo /battery_state"
    ros2 topic echo /battery_state
  else
    echo -e "ros2 topic echo --once --flow-style /battery_state"
    ros2 topic echo --once --flow-style -l 1 /battery_state
fi


