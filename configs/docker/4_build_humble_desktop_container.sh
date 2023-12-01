#!/bin/bash

# First build the basic ros humble desktop image
pushd docker_images/ros/humble/ubuntu/jammy/desktop
sudo docker build -t ros_docker .
popd

# build a ros humble desktop tagged r2hd
cp docker_images/ros/humble/ubuntu/jammy/desktop/Dockerfile docker_files/ros2_humble_desktop_dockerfile
sudo docker build . -t r2hd -f docker_files/ros2_humble_desktop_dockerfile
