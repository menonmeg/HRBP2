

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
    0x51:'MX1', 0x45:'MX2', 0x4E:'MX3', 0x09:'MX4',0x34: 'MX5'
}
MOVE_TORQUE = 0.2
MOVE_DUR = 0.25
WAIT_DUR = 0.2

TURN_TORQUE = 0.2
TURN_DUR = 0.2

X_TORQUE = 5.0

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
	self.r.xmotor.set_torque(0)
	self.r.lservo.set_torque(0)
	self.r.rservo.set_torque(0)

        yield self.forDuration(self.dur)

	self.r.lwheel.set_torque(0)
        self.r.rwheel.set_torque(0)
	self.r.xmotor.set_torque(0)
	self.r.lservo.set_torque(0)
	self.r.rservo.set_torque(0)


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
	self.r.xmotor.set_torque(0)
	self.r.lservo.set_torque(0)
	self.r.rservo.set_torque(0)     

        yield self.forDuration(self.dur)

	self.r.lwheel.set_torque(0)
        self.r.rwheel.set_torque(0)
	self.r.xmotor.set_torque(0)
	self.r.lservo.set_torque(0)
	self.r.rservo.set_torque(0)

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
        self.xSpeed = X_TORQUE

    def behavior(self):
        # Set timeout stamp
        timeout = time.time() + 5.0

        # Set torque to adjust turret
        self.r.xmotor.set_torque(self.xSpeed)        

        # Set torque to 0 after time duration to stop moving
        while True:
            if time.time() > timeout:
                self.r.xmotor.set_torque(0)
                break
     	yield

class DrawingBotApp( JoyApp ):

    def __init__(self, *arg,**kw):
        JoyApp.__init__( self,
          confPath="$/cfg/JoyApp.yml", *arg, **kw
          )

    def onStart(self):
        # Load plans here
        self.moveP = MovePlan(self)
        self.turnP = RotatePlan(self)
	self.xP = XPlan(self)

    def onEvent(self, evt):
        if evt.type != KEYDOWN:
                return

        if evt.type == KEYDOWN:
            if evt.key == K_UP and not self.moveP.isRunning():
                # Forward plan
                self.moveP.torque = -1 * MOVE_TORQUE
                self.moveP.start()
                return progress("(say) Move forward")
            elif evt.key == K_DOWN and not self.moveP.isRunning():
                # Backward plan
                self.moveP.torque = MOVE_TORQUE
                self.moveP.start()
                return progress("(say) Move back")
            elif evt.key == K_LEFT and not self.turnP.isRunning():
                # Turn left plan
                self.turnP.torque = -1 * TURN_TORQUE
                self.turnP.start()
                return progress("(say) Turn left")
            elif evt.key == K_RIGHT and not self.turnP.isRunning():
                # Turn right plan
                self.turnP.torque =  TURN_TORQUE
                self.turnP.start()
                return progress("(say) Turn right")
            elif evt.key == K_m and not (self.turnP.isRunning() or  self.moveP.isRunning()):
                self.xP.turretSpeed = X_TORQUE 
                self.xP.start()
                return progress("(say) adjusted x")
            elif evt.key == K_n and not (self.turnP.isRunning() or  self.moveP.isRunning()):
                self.xP.turretSpeed = -1*X_TORQUE 
                self.xP.start()
                return progress("(say) adjusted x")
	
   

#runs on main
if __name__=="__main__":
    print """
    Running the robot simulator

    Listens on local port 0xBAA (2986) for incoming waypointServer
    information, and also transmits simulated tagStreamer messages to
    the waypointServer.
    """
    import sys
    app=DrawingBotApp(robot = dict(count = 5))
    app.run()
