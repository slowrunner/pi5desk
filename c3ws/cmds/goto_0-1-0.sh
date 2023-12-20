#!/bin/bash


echo -e "\n*** GO TO 1m left of home - 0,1 0 deg at 0.05m/s (5cm/s)"
echo -e 'ros2 action send_goal /navigate_to_position irobot_create_msgs/action/NavigateToPosition "{achieve_goal_heading: true, max_translation_speed: 0.05, max_rotation_speed: 0.5, goal_pose:{pose:{position:{x: 0, y: 1, z: 0}, orientation:{x: 0, y: 0, z: 0, w: 1} }}}"'
ros2 action send_goal /navigate_to_position irobot_create_msgs/action/NavigateToPosition "{achieve_goal_heading: true, max_translation_speed: 0.05, max_rotation_speed: 0.5, goal_pose:{pose:{position:{x: 0, y: 1, z: 0}, orientation:{x: 0, y: 0, z: 0, w: 1} }}}"
