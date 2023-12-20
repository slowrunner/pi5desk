#!/usr/bin/env python3

# FILE: battery_sub.py

"""
    Test running a battery_state subcription 24/7
    - subscribes to Create3 /battery_state and /dock (_status)

    Requires:

    Message Formats:

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

"""

import rclpy
import math
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from rclpy.qos import qos_profile_sensor_data
from rclpy.action import ActionClient
from rclpy.time import Time
from sensor_msgs.msg import BatteryState       # percentage: 0.0 - 1.0

import sys
import logging
import datetime as dt

DEBUG = False

# Uncomment for debug prints to console
DEBUG = True

class BatterySub(Node):

  def __init__(self):
    super().__init__('battery_sub')


    printMsg = '** Battery_Sub node started **'
    print(printMsg)


    self.sub = self.create_subscription(
      BatteryState,
      'battery_state',
      self.battery_state_sub_callback,
      # pick one from following- explicit or named profile
      # QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
      qos_profile_sensor_data)  # best effort depth 10 sensor profile

    if DEBUG:
      dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      printMsg = '\n{}| *** /battery_state subscriber created'.format(dtstr)
      print(printMsg)

    self.battery_state = None


    period_for_timer = 60.0  # Once every 60 seconds
    self.timer = self.create_timer( period_for_timer, self.main_cb)  # call the do nothing call back  when ROS timer triggers
    if DEBUG:
        dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        printMsg ='{}| battery_sub: created main_cb callback for once every {:.0f} seconds'.format(dtstr,period_for_timer)
        print(printMsg)
    self.battery_percentage = -1


  def battery_state_sub_callback(self,battery_state_msg):
    self.battery_state = battery_state_msg
    self.battery_percentage = self.battery_state.percentage
    if DEBUG:
      dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      printMsg = "{}| battery_state_sub_callback(): battery_state.percentage {:.0f} %".format(dtstr, 100 * self.battery_percentage)
      print(printMsg)


  def main_cb(self):
      if DEBUG:
        dtstr = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        printMsg = "{}| main_cb(): executing".format(dtstr)
        print(printMsg)
      else:
        pass



def main():
  rclpy.init(args=None)
  test_node = BatterySub()
  try:
    rclpy.spin(test_node)
  except KeyboardInterrupt:
    pass
  except ExternalShutdownException:
    sys.exit(0)
  finally:
    test_node.destroy_node()
    try:
      rclpy.try_shutdown()
    except:
      pass


if __name__ == '__main__':
    main()
