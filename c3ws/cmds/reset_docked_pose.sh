#!/bin/bash

echo -e '\n****** DOES NOT WORK PROPERLY - ORIENTATION RESET TO 0, should be 180'
echo -e '\n** Reset pose to 0,0 180 (docked)'

if [ $ROS_DISTRO != "galactic" ]; then  
  echo -e '** CURRENT ODOM'
  ros2 topic echo --once --flow-style /odom
fi

echo -e '** SEND RESET_POSE position: x,y,z = 0, Quat: 0,0,1,0'
# ros2 service call /reset_pose irobot_create_msgs/srv/ResetPose "{}"
echo -e 'ros2 service call /reset_pose irobot_create_msgs/srv/ResetPose "pose: {position: {x: 0, y: 0, z: 0}, orientation: {x: 0, y: 0, z: 1, w: 0}}"'
ros2 service call /reset_pose irobot_create_msgs/srv/ResetPose "pose: {position: {x: 0, y: 0, z: 0}, orientation: {x: 0, y: 0, z: 1, w: 0}}"

if [ $ROS_DISTRO != "galactic" ]; then  
  echo -e '** New Odom'
  ros2 topic echo --once --flow-style /odom
fi

echo -e '********\n'
