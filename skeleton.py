# !/usr/bin/env python3
import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header

class DetermineColor(Node):
    def __init__(self):
        super().__init__('color_detector')
        self.image_sub = self.create_subscription(Image, '/color', self.callback, 10)
        self.color_pub = self.create_publisher(Header, '/rotate_cmd', 10)
        self.bridge = CvBridge()
        self.count=0

    def callback(self, data):
    	try:
    		image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
    		cv2.imshow('Image', image)
	    	cv2.waitKey(1)
	    	# prepare rotate_cmd msg
	    	# DO NOT DELETE THE BELOW THREE LINES!
	    	msg = Header()
	    	msg = data.header
	    	msg.frame_id = '+1'  # default: STOP
	
	    	# determine background color
	    	# TODO 
	    	# determine the color and assing +1, 0, or, -1 for frame_id
	    	# msg.frame_id = '+1' # CCW 
	    	# msg.frame_id = '0'  # STOP
	    	# msg.frame_id = '-1' # CW 
	    	
	    	if image[0,0,0]>0:
	    		msg.frame_id = '+1'
	    	if image[0,0,2]>0:
	    		msg.frame_id = '-1'
		 
	    	#publish color_state
	    	self.color_pub.publish(msg)
    		
	    	image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
    	except CvBridgeError as e:
    		self.get_logger().error('Failed to convert image: %s' % e)



if __name__ == '__main__':
    rclpy.init()
    detector = DetermineColor()
    rclpy.spin(detector)
    detector.destroy_node()
    rclpy.shutdown()

