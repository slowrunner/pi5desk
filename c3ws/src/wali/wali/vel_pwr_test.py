#!/usr/bin/env python3

# FILE: vel_pwr_test.py

"""
    Find optimum velocity (in m/s per W) for Create3 Robot
    - subscribes to Create3 /battery_state for voltage, current, and percentage
    - publishes /undock action goal when BatteryState.percentage = 1.0
    - Logs successful undock to life.log
    - calls /navigate_to_position action handler repeatedly if battery.percentage > 20%
      - two out and back 1 meter runs at five speeds between min_vel and max_vel settings
      - uses rotate to face goal, translate with no goal heading
      - during feedback = DRIVING_GOAL_POSITION (2) collects array of battery.voltage and battery.current
      - saves test number, velocity, average voltage, average current, average power
    - rotates to face dock when complete  by publishing rotate_angle 90 cw
    - publishes /dock action goal when BatteryState.percentage < 0.15
    - Logs successful docking to life.log

    Requires:
    - /home/ubuntu/life.log with 666 permission

    Message Formats:

    - irobot_create_msgs/msg/DockStatus.msg
      std_msgs/Header header  # Header stamp is when dock info was queried.
      bool dock_visible       # Whether robot sees dock in its sensors used for docking
      bool is_docked          # Whether the robot is docked

    - sensor_msgs/msg/BatteryState
      std_msgs/Header  header
      	builtin_interfaces/Time stamp
		int32 sec
		uint32 nanosec
	string frame_id
      float32 voltage          # Voltage in Volts (Mandatory)
      float32 temperature      # Temperature in Degrees Celsius (If unmeasured NaN)
      float32 current          # Negative when discharging (A)  (If unmeasured NaN)
      float32 charge           # Current charge in Ah  (If unmeasured NaN)
      float32 capacity         # Capacity in Ah (last full capacity)  (If unmeasured NaN)
      float32 design_capacity  # Capacity in Ah (design capacity)  (If unmeasured NaN)
      float32 percentage       # Charge percentage on 0 to 1 range  (If unmeasured NaN)
      ... and more
    - irobot_create_msgs/action/Undock
      # Request
      ---
      # Result
      bool is_docked
      ---
      # Feedback

    - irobot_create_msgs/action/DockServo
      # Request
      ---
      # Result
      bool is_docked
      ---
      # Feedback
      bool sees_dock

    - irobot_create_msgs/action/RotateAngle
      # Request

      # Rotate for relative angle (radians) from current robot position.  Angles greater than 2 PI will cause the robot to rotate in multiple circles
      float32 angle
      # Max rotation speed (positive rad/s), will cap negative angle to negative speed
      float32 max_rotation_speed 1.9
      ---
      # Result
      # Pose where robot finished
      geometry_msgs/PoseStamped pose
      ---
      # Feedback
      # Remaining radians to rotate
      float32 remaining_angle_travel


    - irobot_create_msgs/action/NavigateToPosition
        # Request

        # Drive to goal position in odometry frame using simple rotate/translate/rotate approach
        geometry_msgs/PoseStamped goal_pose
        # Whether to achieve goal heading for final orientation or just use position
        bool achieve_goal_heading
        # Max translation speed (positive m/s), will cap negative distance to negative speed
        float32 max_translation_speed 0.3
        # Max rotation speed (positive rad/s), will cap negative angle to negative speed
        float32 max_rotation_speed 1.9
        ---
        # Result
        # Pose where robot finished
        geometry_msgs/PoseStamped pose
        ---
        # Feedback
        # Whether robot is in first phase rotating to face travel direction to goal position
        int8 ROTATING_TO_GOAL_POSITION = 1
        # Whether robot is in second phase translating to to goal position
        int8 DRIVING_TO_GOAL_POSITION = 2
        # Whether robot is in third phase rotating to face goal orientation
        int8 ROTATING_TO_GOAL_ORIENTATION = 3
        # Which of the 3 phases above that robot is currently in
        int8 navigate_state
        # Remaining radians to rotate when robot is ROTATING_TO_GOAL_POSITION or ROTATING_TO_GOAL_ORIENTATION
        float32 remaining_angle_travel
        # How much distance is left to travel when robot is DRIVING_TO_GOAL_POSITION
        float32 remaining_travel_distance

"""

import rclpy
import math
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from rclpy.qos import qos_profile_sensor_data
from rclpy.action import ActionClient
from rclpy.time import Time
from sensor_msgs.msg import BatteryState       # percentage: 0.0 - 1.0
from irobot_create_msgs.action import Undock      # no parms, result: is_docked: true,false
# from irobot_create_msgs.msg import DockStatus  # docked: true,false
from irobot_create_msgs.action import DockServo
from irobot_create_msgs.action import RotateAngle  # angle: float32, max_rotation_speed: float32 (1.9r/s), result: pose, Feedback: remaining_angle_travel: float32
from irobot_create_msgs.action import NavigateToPosition # goal_pose, achieve_goal_heading: bool, max_translation_speed: float32, max_rotation_speed: float32
from geometry_msgs.msg import PoseStamped

import sys
import traceback
import logging
import datetime as dt

DEBUG = False
# Uncomment for debug prints to console
DEBUG = True

LIFELOGFILE = "/home/ubuntu/life.log"

UNDOCK_AT_PERCENTAGE = 0.995
ROTATE_AT_PERCENTAGE = 0.20
DOCK_AT_PERCENTAGE   = 0.15


class VelPwrTest(Node):

  def __init__(self):
    super().__init__('vel_pwr_test')

    self.lifeLog = logging.getLogger(__name__)
    self.lifeLog.setLevel(logging.INFO)

    self.loghandler = logging.FileHandler(LIFELOGFILE)
    self.logformatter = logging.Formatter('%(asctime)s|%(filename)s| %(message)s',"%Y-%m-%d %H:%M")
    self.loghandler.setFormatter(self.logformatter)
    self.lifeLog.addHandler(self.loghandler)

    printMsg = '** vel_pwr_test started **'
    print(printMsg)
    self.lifeLog.info(printMsg)


    self.sub = self.create_subscription(
      BatteryState,
      'battery_state',
      self.battery_state_sub_callback,
      # pick one from following- explicit or named profile
      # QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
      qos_profile_sensor_data)  # best effort depth 10 sensor profile

    if DEBUG:
      dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      printMsg = '\n*** /battery_state subscriber created'
      print(dtstr,printMsg)

    self.battery_state = None

    self._undock_action_client = ActionClient(self, Undock, 'undock')
    self._dock_action_client = ActionClient(self, DockServo, 'dock')  # the "dock" action server requires a DockServo.action msg
    self._rotate_angle_action_client = ActionClient(self, RotateAngle, 'rotate_angle')
    self._navigate_to_position_action_client = ActionClient(self, NavigateToPosition, 'navigate_to_position')

    if DEBUG:
      period_for_timer = 60.0  # Once every 5 minutes
    else:
      period_for_timer = 300.0  # Once every 5 minutes

    self.timer = self.create_timer( period_for_timer, self.wali_main_cb)  # call the vel_pwr_test's main loop when ROS timer triggers
    if DEBUG:
        dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        printMsg ='vel_pwr_test: created vel_pwr_test_main callback for once every {:.0f} seconds'.format(period_for_timer)
        print(dtstr,printMsg)
    self.battery_percentage = -1.0
    self.state = "init"
    # self.state = "ready2dock"   # for testing docking


  def battery_state_sub_callback(self,battery_state_msg):
    self.battery_state = battery_state_msg
    self.battery_percentage = self.battery_state.percentage
    if DEBUG:
      dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      printMsg = "battery_state_sub_callback(): battery_state.percentage {:.0f} %".format(100 * self.battery_percentage)
      print(dtstr,printMsg)
      # self.lifeLog.info(printMsg)

  def undock_action_send_goal(self):
    undock_msg = Undock.Goal()
    if DEBUG:
      printMsg = "undock_action_send_goal(): executing"
      print(printMsg)
    self._undock_action_client.wait_for_server()
    self._undock_action_send_goal_future = self._undock_action_client.send_goal_async(undock_msg)
    self._undock_action_send_goal_future.add_done_callback(self.undock_goal_response_callback)

  def undock_goal_response_callback(self, future):
    goal_handle = future.result()
    if DEBUG:
      dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      printMsg = "undock_goal_response_callback(): Goal Accepted: {}".format(goal_handle.accepted)
      print(dtstr,printMsg)

    if not goal_handle.accepted:
      self.get_logger().info('Undock Goal Rejected :(')
      return

    self.get_logger().info('Undock Goal Accepted :)')

    self._get_undock_result_future = goal_handle.get_result_async()
    self._get_undock_result_future.add_done_callback(self.get_undock_result_callback)

  def get_undock_result_callback(self, future):
    result = future.result().result
    if DEBUG:
      dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      printMsg = "get_undock_result_callback(): Undock Result is_docked {} %".format(result.is_docked)
      print(dtstr, printMsg)

    if result.is_docked:
      self.state = "docked"
      printMsg = "** WaLI Undocking: failed **"
      if DEBUG:
          dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          print(dtstr, printMsg)
      self.lifeLog.info(printMsg)

    else:
      self.state = "undocked"
      printMsg = "** WaLI Undocking: success at battery {:.0f}% **".format(self.battery_percentage*100)
      self.lifeLog.info(printMsg)
      if DEBUG:
          dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          print(dtstr, printMsg)

  # #################### NAVIGATE TO POSITION #####################
  def navigate_to_position_action_send_goal(self,goal,speed):
    navigate_to_position_msg = navigate_to_position.Goal()
    navigate_to_position_msg.goal_pose = PoseStamped()
    navigate_to_position_msg.goal_pose.header.seq = 1
    navigate_to_position_msg.goal_pose.header.stamp = self.get_clock().now().to_msg()
    navigate_to_position_msg.goal_pose.position.x = 0.100
    navigate_to_position_msg.goal_pose.position.y = 0.500
    navigate_to_position_msg.achieve_goal_heading = false
    navigate_to_position_msg.max_translation_speed = speed
    navigate_to_position_msg.max_rotation_speed = 1.0



    if DEBUG:
      printMsg = "navigate_to_position_action_send_goal({:.2f}m/s): executing".format(speed)
      print(printMsg)
    self.state = "at_goal"
    self._navigate_to_position_action_client.wait_for_server()
    self._navigate_to_position_action_send_goal_future = self._navigate_to_position_action_client.send_goal_async(navigate_to_position_msg)
    self._navigate_to_position_action_send_goal_future.add_done_callback(self.navigate_to_position_goal_response_callback)

  def navigate_to_position_goal_response_callback(self, future):
    goal_handle = future.result()
    if DEBUG:
      dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      printMsg = "navigate_to_position_goal_response_callback(): Goal Accepted: {}".format(goal_handle.accepted)
      print(dtstr,printMsg)

    if not goal_handle.accepted:
      self.get_logger().info('navigate_to_position Goal Rejected :(')
      return

    self.get_logger().info('navigate_to_position Goal Accepted :)')
    self.state = "nav_to_goal"
    self._get_navigate_to_position_result_future = goal_handle.get_result_async()
    self._get_navigate_to_position_result_future.add_done_callback(self.get_navigate_to_position_result_callback)

  def get_navigate_to_position_result_callback(self, future):
    result = future.result().result
    self.state = "at_goal"
    printMsg = "** WaLI nav_to_pos: at_goal result x: {:.3f} y: {:.3f} **".format(result.pose.x, result.pose.y)
    if DEBUG:
          dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          print(dtstr, printMsg)
    self.lifeLog.info(printMsg)


  # ############################# DOCK ACTION #############################

  def dock_action_send_goal(self):
    dock_msg = DockServo.Goal()
    if DEBUG:
      dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      printMsg = "dock_action_send_goal(): executing"
      print(dtstr, printMsg)
    self._dock_action_client.wait_for_server()
    if DEBUG:
        dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(dtstr, "dock_action_send_goal(): after wait_for_server()")
    self._dock_action_send_goal_future = self._dock_action_client.send_goal_async(dock_msg)
    if DEBUG:
        dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(dtstr, "dock_action_send_goal(): after set future")
    self._dock_action_send_goal_future.add_done_callback(self.dock_goal_response_callback)
    if DEBUG:
        dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(dtstr, "dock_action_send_goal(): after add_done_callback")

  def dock_goal_response_callback(self, future):
    goal_handle = future.result()
    if DEBUG:
      dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      printMsg = "dock_goal_response_callback(): Goal Accepted: {}".format(goal_handle.accepted)
      print(dtstr, printMsg)

    if not goal_handle.accepted:
      printMsg = 'dock Goal Rejected'
      self.get_logger().info(printMsg)
      if DEBUG:
          dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          print(dtstr, printMsg)
      return

    printMsg = 'dock Goal Accepted'
    self.get_logger().info(printMsg)
    if DEBUG:
        dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(dtstr, printMsg)

    self.state = "docking"

    self._get_dock_result_future = goal_handle.get_result_async()
    self._get_dock_result_future.add_done_callback(self.get_dock_result_callback)

  def get_dock_result_callback(self, future):
    result = future.result().result
    if DEBUG:
      dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      printMsg = "get_dock_result_callback(): dock Result is_docked {} %".format(result.is_docked)
      print(dtstr, printMsg)
    if result.is_docked:
      dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      self.state = "docked"
      printMsg = "** WaLI Docking: success at battery {:.0f}% **".format(self.battery_percentage*100)
      self.lifeLog.info(printMsg)
      if DEBUG:
          dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          print(dtstr, printMsg)
    else:
      self.state = "undocked"
      printMsg = "** WaLi Docking: failed **"
      self.lifeLog.info(printMsg)
      if DEBUG:
          dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          print(dtstr, printMsg)


  # ################## ROTATE ANGLE #################################

  def rotate_angle_action_send_goal(self,angle):
    rotate_angle_msg = RotateAngle.Goal()
    rotate_angle_msg.angle = angle

    if DEBUG:
      printMsg = "rotate_angle_action_send_goal(rotate_angle_msg.angle={:.3f}): executing".format(rotate_angle_msg.angle)
      print(printMsg)
    self._rotate_angle_action_client.wait_for_server()
    self._rotate_angle_action_send_goal_future = self._rotate_angle_action_client.send_goal_async(rotate_angle_msg)
    self._rotate_angle_action_send_goal_future.add_done_callback(self.rotate_angle_goal_response_callback)

  def rotate_angle_goal_response_callback(self, future):
    goal_handle = future.result()
    if DEBUG:
      printMsg = "rotate_angle_goal_response_callback(): Goal Accepted: {}".format(goal_handle.accepted)
      print(printMsg)

    if not goal_handle.accepted:
      self.get_logger().info('rotate Goal Rejected :(')
      return

    self.get_logger().info('rotate Goal Accepted :)')

    self._get_rotate_angle_result_future = goal_handle.get_result_async()
    self._get_rotate_angle_result_future.add_done_callback(self.get_rotate_angle_result_callback)

  def get_rotate_angle_result_callback(self, future):
    result = future.result().result
    if DEBUG:
      printMsg = "get_rotate_angle_result_callback(): rotate Result {} %".format(result)
      print(printMsg)
    # if result.is_rotateed:
    #    self.state = "ready2dock"
    # else:
    #  # do not change WaLI state
    #  pass
    # self.get_logger().info('Result: {0}'.format(result))


  # ################# MAIN CALL BACK #################################

  def wali_main_cb(self):
    try:
      if DEBUG:
        dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        printMsg = "vel_pwr_test_main_cb(): executing"
        print(dtstr, printMsg)
        printMsg = "vel_pwr_test_main_cb(): wali.state = {}".format(self.state)
        print(dtstr, printMsg)

      # WaLI logic
      # publishes /undock action goal when BatteryState.percentage at or near full (and state="docked")
      # publishes /rotate_angle {angle: 1.57} (180deg) when BatteryState.percentage low
      # publishes /dock action goal when BatteryState.percentage very low
      #
      # OTHERWISE 
      #      speed = speed_list[loopcount]
      #      goal_position = goal_position_list[loop_count % 2]
      #      call NavigateToPosition action goal with speed and goal_position
      #      wait for state = at_goal
      #        log goal complete, ave volt, ave current, total power, drive_power
      

      if (self.battery_percentage > UNDOCK_AT_PERCENTAGE) and (self.state in ["docked","init"]):
        self.state = "undocking"
        if DEBUG:
          dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          printMsg = "wali_main_cb(): battery_percentage {:.0} % sending undock action goal".format(self.battery_percentage)
          print(dtstr, printMsg)
        self.undock_action_send_goal()

      elif (self.battery_percentage < ROTATE_AT_PERCENTAGE) and (self.state in ["undocked","init"]):
        self.state = "turning"
        if DEBUG:
           dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           printMsg = "wali_main_cb(): battery_percentage {:.0} % sending rotate180 action goal".format(self.battery_percentage)
           print(dtstr, printMsg)
        self.rotate_angle_action_send_goal(angle=math.pi)    # pi=180 deg
        self.state = "ready2dock"

      elif (self.battery_percentage < DOCK_AT_PERCENTAGE) and (self.state in ["ready2dock"]):
        self.state = "docking"
        if DEBUG:
           dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           printMsg = "wali_main_cb(): battery_percentage {:.0} % sending dock action goal".format(self.battery_percentage)
           print(dtstr, printMsg)
        self.dock_action_send_goal()

      elif (self.state in ["init", "undocked","at_goal"]):
        if DEBUG:
           dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           printMsg = "wali_main_cb(): loop count {} % sending nav_to_pos action goal".format(self.loop_count)
           print(dtstr, printMsg)
        goal=[0,0.300]
        speed = 0.1
        self.navigate_to_position_action_send_goal(goal,speed)
        self.loop_count += 1


    except Exception as e:
        print("wali_main_cb(): Exception:",str(e))
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)

# ################### MAIN ###############################
def main():
  rclpy.init(args=None)
  vel_pwr_test = VelPwrTest()
  vel_pwr_test.loop_count = 0
  try:
    rclpy.spin(vel_pwr_test)
  except KeyboardInterrupt:
    pass
  except ExternalShutdownException:
    sys.exit(0)
  finally:
    vel_pwr_test.destroy_node()
    try:
      rclpy.try_shutdown()
    except:
      pass


if __name__ == '__main__':
    main()
