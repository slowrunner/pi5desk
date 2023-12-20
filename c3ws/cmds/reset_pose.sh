#!/bin/bash

# Note: not implemented in simulator, docs say "implemented in G.3.1"

echo -e '\n** Fix Odom Drift with reset_pose 0,0/0'

if [ $ROS_DISTRO != "galactic" ]; then  
  echo -e '** CURRENT ODOM'
  ros2 topic echo --once --flow-style /odom
fi

echo -e '** SEND RESET_POSE'
ros2 service call /reset_pose irobot_create_msgs/srv/ResetPose "{}"

# To Reset To particular pose:
# ros2 service call /reset_pose irobot_create_msgs/srv/ResetPose "pose: {position: {x: 1, y: 2, z: 0}, orientation: {x: 0, y: 0, z: 0, w: 1}}"

if [ $ROS_DISTRO != "galactic" ]; then  
  echo -e '** New Odom'
  ros2 topic echo --once --flow-style /odom
fi

echo -e '********\n'
