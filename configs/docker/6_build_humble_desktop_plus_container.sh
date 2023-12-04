#!/bin/bash

# Process to build r2hdp under docker_images/
# mv docker_images/ros/humble/ubuntu/jammy/desktop/Dockerfile docker_images/ros/humble/ubuntu/jammy/desktop/Dockerfile.ros_humble_desktop_dockerfile
# cp docker_files/ros2_humble_desktop_plus_nav_dockerfile docker_images/ros/humble/ubuntu/jammy/desktop/Dockerfile
# pushd docker_images/ros/humble/ubuntu/jammy/desktop
# sudo docker build -t r2hdp .
# popd


# build a ros humble desktop plus navigation, slam-toolbox, localization tagged r2hdp
sudo docker build . -t r2hdp -f docker_files/ros2_humble_desktop_plus_dockerfile
