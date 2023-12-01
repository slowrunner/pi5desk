#!/bin/bash

# First build the basic ros humble desktop image tagged r2hd
pushd docker_images/ros/humble/ubuntu/jammy/desktop
# original: sudo docker build -t ros_docker .
sudo docker build -t r2hd .
popd

# build a ros humble desktop tagged r2hd
cp docker_images/ros/humble/ubuntu/jammy/desktop/Dockerfile docker_files/ros2_humble_desktop_dockerfile
# original: required ros_docker built
# sudo docker build . -t r2hd -f docker_files/ros2_humble_desktop_dockerfile
