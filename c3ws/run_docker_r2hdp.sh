#!/bin/bash

cd ~/pi5desk/c3ws
# --rm removes container after exit
# --w working dir to start in
echo -e "\n*** STARTING ROS 2 HUMBLE PLUS IN DOCKER ***"
docker run -it --net=host  -v /home/pi:/home/pi -w /home/pi/pi5desk/c3ws --rm r2hdp
echo -e "\n*** EXITED DOCKER ***"
