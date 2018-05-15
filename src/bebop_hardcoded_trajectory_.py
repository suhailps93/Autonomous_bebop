#!/usr/bin/env python 

#import library ros 
import rospy 
import time
import sys
import math
#import library untuk mengirim command dan menerima data navigasi dari quadcopter
from geometry_msgs.msg import Twist
from std_msgs.msg import String 
from std_msgs.msg import Empty 
from std_msgs.msg import UInt8
#from ardrone_autonomy.msg import Navdata

#import class status untuk menentukan status ddari quadcopter
#from drone_status import DroneStatus

COMMAND_PERIOD = 1000


class AutonomousFlight():
    def __init__(self):
        self.status = ""
        rospy.init_node('forward', anonymous=False)
        self.rate = rospy.Rate(10)
        self.pubTakeoff = rospy.Publisher("bebop/takeoff",Empty, queue_size=10)
        self.pubLand = rospy.Publisher("bebop/land",Empty, queue_size=10)
        self.pubCommand = rospy.Publisher('bebop/cmd_vel',Twist, queue_size=10)
        self.pubFlip = rospy.Publisher('bebop/flip',UInt8, queue_size=10)
        self.command = Twist()
        #self.commandTimer = rospy.Timer(rospy.Duration(COMMAND_PERIOD/1000.0),self.SendCommand)
        self.state_change_time = rospy.Time.now()    
        rospy.on_shutdown(self.SendLand)

    def SendTakeOff(self):
        self.pubTakeoff.publish(Empty())
        print("takeoff")
        self.rate.sleep()
                
    def SendLand(self):
        self.pubLand.publish(Empty())
        print("landing")
		
    
    def FlipMe(self, data): # Only for Bebop; 0 - flip forward, 1 - flip backward, 2 - flip right, 3 - flip left
        self.pubFlip.publish(UInt8(data))
   
		       
    def SetCommand(self, linear_x, linear_y, linear_z, angular_x, angular_y, angular_z):
        self.command.linear.x = linear_x #Forward & Backward
        self.command.linear.y = linear_y #Left (+) & Right (-)
        self.command.linear.z = linear_z #Up & Down
        self.command.angular.x = angular_x
        self.command.angular.y = angular_y
        self.command.angular.z = angular_z #Clockwise (-) & Anti-Clockwise (+)
        self.pubCommand.publish(self.command)
        self.rate.sleep()

    def Stay(self, T):
	    self.SetCommand(0,0,0,0,0,0)
	    time.sleep(T)

    def Forward(self, s):
		v = 1
		t = s / v
		for i in range(int(10 * t)):
			self.SetCommand(1,0,0,0,0,0)
			print("Go forward" + str(i))

    def Backward(self, s):
		v = 1
		t = s / v
		for i in range(int(10 * t)):
			self.SetCommand(-1,0,0,0,0,0)
			print("Go backward" + str(i))

    def goLeft(self, s):
		v = 1
		t = s / v
		for i in range(int(10 * t)):
			self.SetCommand(0,1,0,0,0,0)
			print("Go backward" + str(i))

    def Vclimb(self, s):
		v = 1
		t = s / v
		for i in range(int(10 * t)):
			self.SetCommand(0,0,1,0,0,0)
			print("Go backward" + str(i))
    
    def goRight(self, s):
		v = 1
		t = s / v
		for i in range(int(10 * t)):
			self.SetCommand(0,-1,0,0,0,0)
			print("Go backward" + str(i))   
  
    def Turnright(self, deg):
		rad = deg * (math.pi / 180)
		t = int(10*rad)
		for i in range(t):
			self.SetCommand(0,0,0,0,0,1)
		print("Turning " + str(deg) + " deg")

    def Turnleft(self, deg):
		rad = deg * (math.pi / 180)
		t = int(10*rad)
		for i in range(t):
			self.SetCommand(0,0,0,0,0,-1)
		print("Turning " + str(deg) + " deg")


    def spiral(self, r, t): # testing a small circle
		circum = 2 * math.pi * r
		v = circum / t
		w = v / r
		for i in range(int(t * 10/2)):
			self.SetCommand(v,0,0.1,0,0,w)
			print("spiralling " + str(i))
			
    def circle(self, r, t): # testing a small circle
		circum = 2 * math.pi * r
		v = circum / t
		w = v / r
		for i in range(int(t * 10)):
			self.SetCommand(v,0,0,0,0,w)
			print("circle " + str(i))
						




if __name__ == '__main__': 
    try: 
        
        uav = AutonomousFlight()
        count = 0    
        while not rospy.is_shutdown():
			i = 0
			uav.SendTakeOff()
			uav.Stay(1)
			if count == 2:
				uav.circle(1, 10)
				uav.Stay(3)
				uav.SendLand()
				sys.exit()
			count+=1


    	
		
         
    except rospy.ROSInterruptException:
        pass
