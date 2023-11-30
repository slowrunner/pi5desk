# First Test

# Create ros2ws/src directory
mkdir -p ~/pi5desk/ros2ws/src
cd ~/pi5desk/ros2ws

# start Docker mounting ros2ws
docker run -it --net=host  -v ~/pi5desk/ros2ws:/ros2ws r2hd

   cd /ros2ws
   ros2 pkg list
   ros2 run demo_nodes_cpp listener & ros2 run demo_nodes_cpp talker
   cntrl-c
   ps -ef | grep ros
   kill x y


# If have ROS 2 Humble robot available
pi5desk:
cd ~/pi5desk/ros2ws

# start Docker
docker run -it --net=host  -v ~/pi5desk/ros2ws:/ros2ws r2hd

   cd /ros2ws
   ros2 run demo_nodes_cpp listener


Robot:
cd ~/HumbleDave/ros2ws
ros2 run demo_nodes_cpp talker

ctrl-c to stop

pi5desk:

ctrl-c to stop
exit   to quit docker
