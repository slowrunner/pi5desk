# Install ROS 2 Humble To Pi5 PiOS Bookworm In Docker

REF: https://docs.ros.org/en/humble/How-To-Guides/Installing-on-Raspberry-Pi.html#raspberry-pi-os-with-ros-2-in-docker

** install Docker
- 1_setup_docker_apt_repo.sh
- 2__install_docker_pkgs.sh 

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm64v8)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.


- 3_clone_ros_docker_images.sh  
- 4_build_humble_desktop_container.sh  

- 5_run_ROS2_Humble_Docker_image.sh


- test: docker run hello-world

"Mount" current working directory to docker environment when launching Docker:
```
-v `pwd`:`pwd` \
```
(if Windows replace pwd with %cd% )

Keep a ROS Docker alive - start in detached mode
- docker run -dt --name robot_env --restart unless-stopped r2hd

Connect or reconnect to the running Docker environment:
-docker exec -it robot_env bash

Shut the detached Docker environment down:
-docker stop robot_env && docker rm robot_env

Reuse last container if stopped or docker restarted or computer rebooted:
docker start robot_env

Check if container alive:
docker container ls -a

