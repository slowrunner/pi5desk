#!/bin/bash

pushd docker_images/ros/humble/ubuntu/jammy/desktop
sudo docker build -t ros_docker .
popd
cp docker_images/ros/humble/ubuntu/jammy/desktop/Dockerfile ros2_humble_desktop_dockerfile
sudo docker build . -t r2hd -f ros2_humble_desktop_dockerfile
