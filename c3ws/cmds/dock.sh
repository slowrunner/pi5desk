#!/bin/bash

echo -e "\n** DOCK **"
if [ $ROS_DISTRO == "galactic" ]
  then
    echo -e '** ros2 action send_goal /dock irobot_create_msgs/action/DockServo "{}"'
    ros2 action send_goal /dock irobot_create_msgs/action/DockServo "{}"
  else
    echo -e '** ros2 action send_goal /dock irobot_create_msgs/action/Dock "{}"'
    ros2 action send_goal /dock irobot_create_msgs/action/Dock "{}"
fi



