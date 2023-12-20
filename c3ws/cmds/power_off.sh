#!/bin/bash

echo -e "\n*** POWER OFF ***"

read -p "Are you sure? " -n 1 -r
# echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # do dangerous stuff
    echo "ros2 service call robot_power irobot_create_msgs/srv/RobotPower"
    ros2 service call robot_power irobot_create_msgs/srv/RobotPower
    echo "Success=false is not a problem"
fi
