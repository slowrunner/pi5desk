'''
sub_ir.py
Tufts Create®3 Educational Robot Example
by Kate Wujciak 

Modified to provide approximate distance value for readings: cyclicalobsessive
  requires adding to setup.py:datafiles =
       ('lib/' + package_name, [package_name+'/create3_ir_dist.py']),
  to cause import to be copied to install package when building

This file shows how to subscribe to a topic in ROS2 using the Create®3. It subscribes
to the IR sensor and displays the relevant information in your terminal. 
'''

import sys
import rclpy
import create3_ir_dist

'''
Statements that import messages, actions, interfaces, and variable types.
'''
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from irobot_create_msgs.msg import IrIntensityVector

'''
Input your namespace here as a global variable. 
'''
# namespace = '[Namespace]'
namespace = ''

class IRSubscriber(Node):
    '''
    The IRSubscriber class is created which is a subclass of Node.
    The Node is subscribing to the /ir_intensity topic.
    '''
    
    def __init__(self):
        '''
        The following line calls the Node class' constructor and declares a node name,
        which is 'IR_subscriber' in this case. 
        '''
        super().__init__('IR_subscriber')
        '''
        This line indicates that the node is subscribing to the IrIntensityVector
        type over the '/ir_intensity' topic. 
        '''
        print('Creating subscription to to the IrIntensityVector type over the /ir_intensity topic')
        self.subscription = self.create_subscription(
            IrIntensityVector, namespace + '/ir_intensity', self.listener_callback,
            qos_profile_sensor_data)

        # rolling counter (0-61) of ir_intensity msgs received from 62 Hz topic
        self.ir_intensity_counter = 0


    def listener_callback(self, msg:IrIntensityVector):
        '''
        The subscriber's callback listens and as soon as it receives the message,
        this function runs. 
        This callback function is basically printing what it hears. It runs the data
        it receives in your terminal (msg).  
        '''
        # print('Now listening to IR sensor readings it hears...')

        if (self.ir_intensity_counter == 0):  # Print values each time counter is 0
          self.printIR(msg)

        # increment/roll msg counter approximately once each second for 62 Hz topic
        self.ir_intensity_counter = (self.ir_intensity_counter + 1) % 62


    def printIR(self, msg):
        '''
        This function is used in the above function. Its purpose is to determine 
        which parts of the info are worth showing.
        :type msg: IrIntensity
        :rtype: None
        The msg is returned from our topic '/ir_intensity.'
        To get components of a message, use the '.' dot operator. 
        '''

        labels = ["side_left", "left", "front_left", "front_center_left", "front_center_right", "front_right", "right"]
        label_idx = 0
        print('\nCreate3 IR sensor:')
        for reading in msg.readings: 
        	val = reading.value
        	dist = create3_ir_dist.dist_ir_reading(label_idx,val)
        	label = labels[label_idx]
        	print("{:<20} intensity: {:>5} dist: {:>-8.3f}m".format(label,str(val),dist) )
        	label_idx += 1

def main(args=None):
    '''
    This line initializes the rclpy library. 
    '''
    rclpy.init(args=args)
    '''
    This creates the node.
    '''
    IR_subscriber = IRSubscriber()
    '''
    The node is then "spun" so its callbacks are called.
    '''
    print('Callbacks are called.')
    try:
        rclpy.spin(IR_subscriber)
    except KeyboardInterrupt:
        print('\nCaught keyboard interrupt')
    finally:
    	'''
    	Destroying the node acts as a "reset" so we don't run into 
    	any problems when we try and run again.
    	'''
    	print("Done")
    	IR_subscriber.destroy_node()
    	# rclpy.shutdown()


if __name__ == '__main__':
    main()
