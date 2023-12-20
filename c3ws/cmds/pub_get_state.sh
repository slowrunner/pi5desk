#!/bin/bash

echo -e "\n*** PUB get_state"
echo -e 'ros2 service call /get_state lifecycle_msgs/srv/GetState "{}"'
ros2 service call /get_state lifecycle_msgs/srv/GetState "{}"
