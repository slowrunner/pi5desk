#!/bin/bash


echo -e "\n*** GOTO 0.8,0  0 deg"
echo -e 'ros2 action send_goal /navigate_to_position irobot_create_msgs/action/NavigateToPosition "{achieve_goal_heading: true, max_translation_speed: 0.1, max_rotation_speed: 0.5, goal_pose:{pose:{position:{x: 0.8,y: 0,z: 0.0}, orientation:{x: 0.0,y: 0.0, z: 0, w: 1}}}}"'
ros2 action send_goal /navigate_to_position irobot_create_msgs/action/NavigateToPosition "{achieve_goal_heading: true, max_translation_speed: 0.1, max_rotation_speed: 0.5, goal_pose:{pose:{position:{x: 0.8, y: 0.0,z: 0.0}, orientation:{x: 0,y: 0, z: 0, w: 1}}}}"
