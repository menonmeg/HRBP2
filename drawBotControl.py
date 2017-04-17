

# -*- coding: utf-8 -*-
"""
File: drawBotControl.py
authors: menonmeg
"""
from joy import JoyApp, progress
from joy.decl import *
from joy.plans import Plan
from socket import (
  socket, AF_INET,SOCK_DGRAM, IPPROTO_UDP, error as SocketError,
  )
from syncmx import *
from joy import *
import time

SERVO_NAMES = {
    0x51:'MX1', 0x45:'MX2', 0x4E:'MX3', 0x09:'MX4',0x34: 'MX5', 0x4F: 'M6'
}
MOVE_TORQUE = 0.2
MOVE_DUR = 0.25
WAIT_DUR = 0.2

TURN_TORQUE = 0.2
TURN_DUR = 0.2

X_TORQUE = 0.95
X_DUR = 0.5

Y_TORQUE = 0.2
Y_DUR = 0.2

SERVO_POS = 200

X_DUR_SQUARE = 70
Y_DUR_SQUARE = 5.0



class MovePlan( Plan ):
    """
    Plan that moves buggy forward or backward by setting equal torque on wheels
    for a fixed duration of time.

    Torque and Duration are public variables that can be modified on the fly.
    To move buggy backwards set torque to a negative value.
    """

    def __init__(self,app):
	Plan.__init__(self,app)
        self.r = self.app.robot.at
        self.torque = MOVE_TORQUE
        self.dur = MOVE_DUR


    def behavior(self):
        # Set torque to move wheels. Right wheel must be opposite of left wheel
        # due to orientation of motors
        self.r.lwheel.set_torque(-1*self.torque)
        self.r.rwheel.set_torque(self.torque)

        yield self.forDuration(self.dur)

	self.r.lwheel.set_torque(0)
        self.r.rwheel.set_torque(0)

class RotatePlan( Plan ):
    """
    Plant that rotates buggy by setting torque on wheels for fixed duration.

    Torque and direction are public so they can be modified to change direction
    and speed of rotation. To rotate buggy in opposite direction make torque a
    negative number.
    """

    def __init__(self,app):
        Plan.__init__(self,app)
        self.r = self.app.robot.at
        self.torque = TURN_TORQUE
        self.dur = TURN_DUR
        self.wait = WAIT_DUR


    def behavior(self):

        # Set torque to move wheels. Motors are oriented to move in opposite
        # directions with same torque
        self.r.lwheel.set_torque(self.torque)
        self.r.rwheel.set_torque(self.torque)   

        yield self.forDuration(self.dur)

	self.r.lwheel.set_torque(0)
        self.r.rwheel.set_torque(0)
class AutoPlan( Plan ):
    """
    Plant that rotates buggy by setting torque on wheels for fixed duration.

    Torque and direction are public so they can be modified to change direction
    and speed of rotation. To rotate buggy in opposite direction make torque a
    negative number.
    """

    def __init__(self,app):
        Plan.__init__(self,app)
        self.r = self.app.robot.at
        self.xtorque = X_TORQUE
	self.durX = X_DUR_SQUARE
	self.ytorque = Y_TORQUE
	self.durY = Y_DUR_SQUARE

    def behavior(self):
       
        # Set torque to adjust turret
        self.r.xmotor.set_torque(self.xtorque)        
	
	yield self.forDuration(self.durX)

	self.r.xmotor.set_torque(0) 
	self.r.ymotor.set_torque(self.ytorque) 
	
	yield self.forDuration(self.durY)

	self.r.ymotor.set_torque(0) 
	self.r.xmotor.set_torque(-1*self.xtorque)

	yield self.forDuration(self.durX)

	self.r.xmotor.set_torque(0) 
	self.r.ymotor.set_torque(-1*self.ytorque) 
	
	yield self.forDuration(self.durY)

	self.r.xmotor.set_torque(0) 
	self.r.ymotor.set_torque(0) 
	

class XPlan( Plan ):
    """
    Plant that rotates buggy by setting torque on wheels for fixed duration.

    Torque and direction are public so they can be modified to change direction
    and speed of rotation. To rotate buggy in opposite direction make torque a
    negative number.
    """

    def __init__(self,app):
        Plan.__init__(self,app)
        self.r = self.app.robot.at
        self.xtorque = X_TORQUE
	self.dur = X_DUR

    def behavior(self):
       
        # Set torque to adjust turret
        self.r.xmotor.set_torque(self.xtorque)        
	
	yield self.forDuration(self.dur)

	self.r.xmotor.set_torque(0) 

class YPlan( Plan ):
    """
    Plant that rotates buggy by setting torque on wheels for fixed duration.

    Torque and direction are public so they can be modified to change direction
    and speed of rotation. To rotate buggy in opposite direction make torque a
    negative number.
    """

    def __init__(self,app):
        Plan.__init__(self,app)
        self.r = self.app.robot.at
        self.ytorque = Y_TORQUE
	self.dur = Y_DUR

    def behavior(self):
       
        # Set torque to adjust turret
        self.r.ymotor.set_torque(self.ytorque)        
	
	yield self.forDuration(self.dur)

	self.r.ymotor.set_torque(0) 

class ServoPlan( Plan ):
    """
    Plan that moves buggy forward or backward by setting equal torque on wheels
    for a fixed duration of time.

    Torque and Duration are public variables that can be modified on the fly.
    To move buggy backwards set torque to a negative value.
    """

    def __init__(self,app):
	Plan.__init__(self,app)
        self.r = self.app.robot.at
        self.pos = SERVO_POS
        self.dur = MOVE_DUR


    def behavior(self):
        # Set torque to move wheels. Right wheel must be opposite of left wheel
        # due to orientation of motors

	self.r.lservo.set_pos(self.r.lservo.get_pos() + (-1*self.pos))
        self.r.rservo.set_pos(self.r.rservo.get_pos() + self.pos)

	yield self.forDuration(self.dur)

class StopPlan( Plan ):
    """
    Plant that rotates buggy by setting torque on wheels for fixed duration.

    Torque and direction are public so they can be modified to change direction
    and speed of rotation. To rotate buggy in opposite direction make torque a
    negative number.
    """

    def __init__(self,app):
        Plan.__init__(self,app)
        self.r = self.app.robot.at
	self.dur = MOVE_DUR

    def behavior(self):      

	self.r.ymotor.set_torque(0) 
	self.r.xmotor.set_torque(0) 
	self.r.lwheel.set_torque(0)
        self.r.rwheel.set_torque(0)

	yield self.forDuration(self.dur)

	self.r.ymotor.set_torque(0) 
	self.r.xmotor.set_torque(0) 
	self.r.lwheel.set_torque(0)
        self.r.rwheel.set_torque(0)



class DrawingBotApp( JoyApp ):
	

    def __init__(self, *arg,**kw):
        JoyApp.__init__( self,
          confPath="$/cfg/JoyApp.yml",*arg, **kw 
          )

    def onStart(self):
        # Load plans here
        self.moveP = MovePlan(self)
        self.turnP = RotatePlan(self)
	self.xP = XPlan(self)
	self.yP = YPlan(self)
	self.servoP = ServoPlan(self)
	self.stopP = StopPlan(self)
	self.autoP = AutoPlan(self)

    def onEvent(self, evt):
        if evt.type != KEYDOWN:
                return

        if evt.type == KEYDOWN:
            if evt.key == K_UP:
                # Forward plan
                self.moveP.torque = -1 * MOVE_TORQUE
                self.moveP.start()
                return progress("(say) Move forward")
            elif evt.key == K_DOWN:
                # Backward plan
                self.moveP.torque = MOVE_TORQUE
                self.moveP.start()
                return progress("(say) Move back")
            elif evt.key == K_LEFT:
                # Turn left plan
                self.turnP.torque = -1 * TURN_TORQUE
                self.turnP.start()
                return progress("(say) Turn left")
            elif evt.key == K_RIGHT:
                # Turn right plan
                self.turnP.torque =  TURN_TORQUE
                self.turnP.start()
                return progress("(say) Turn right")
            elif evt.key == K_m:
                self.xP.xtorque = X_TORQUE 
                self.xP.start()
                return progress("(say) adjusted x")
            elif evt.key == K_n:
                self.xP.xtorque = -1 * X_TORQUE 
                self.xP.start()
                return progress("(say) adjusted x")
	    elif evt.key == K_k:
                self.yP.ytorque = Y_TORQUE 
                self.yP.start()
                return progress("(say) adjusted y")
            elif evt.key == K_j:
                self.yP.ytorque = -1 * Y_TORQUE 
                self.yP.start()
                return progress("(say) adjusted y")
	    elif evt.key == K_z:
		self.servoP.pos = SERVO_POS
		self.servoP.start()
	    elif evt.key == K_x:
		self.servoP.pos = -1*SERVO_POS
		self.servoP.start()
	    elif evt.key == K_SPACE:
		self.stopP.start()
	    elif evt.key == K_a:
		self.autoP.start()
		return progress("(say) adjusted y")
	
	
   

#runs on main
if __name__=="__main__":
    import sys
    app=DrawingBotApp(robot = dict(count = 6))
    app.run()
