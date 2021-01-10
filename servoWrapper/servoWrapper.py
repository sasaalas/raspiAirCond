#!/usr/bin/env python

import sys, os.path
servo_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/pwmServoDriver/')
sys.path.append(servo_dir)
from Raspi_PWM_Servo_Driver import PWM

import time
import syslog
import paho.mqtt.client as mqtt

syslog.openlog(sys.argv[0])
 
# Get the total number of args passed to the demo.py
total = len(sys.argv)

if (total != 3):
 print ("servoWrapper: Incorrect parameters.");
 syslog.closelog()
 sys.exit()

userDegree = int(sys.argv[1])
userTime = int(sys.argv[2])
mqttBrokerUrlPath = "your-broker-path"
mqttBrokerPort = 1883
mqttUserName = "your-broker-username-here"
mqttPassword = "your-broker-password-here"


# Initialise the PWM device using the default address
pwm = PWM(0x6F, debug=False)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096
maxDegree = 60 # Degrees your servo can rotate
defaultDegree = 30

pwm.setPWMFreq(60) # Set PWM frequency to 60Hz

def setDegree(channel, d):
    degreePulse = servoMin
    degreePulse += int((servoMax - servoMin) / maxDegree) * d
    pwm.setPWM(channel, 0, degreePulse)

if userDegree > maxDegree:
  userDegree = maxDegree

if userDegree < 0:
  userDegree = 0

if userTime > 0:
 syslog.syslog(syslog.LOG_NOTICE, "servoWrapper: Setting servo degree to: %d" % userDegree)
 setDegree(0, userDegree)
 syslog.syslog(syslog.LOG_NOTICE, "servoWrapper: Sleeping: %d" % userTime)
 time.sleep(userTime)
 syslog.syslog(syslog.LOG_NOTICE, "servoWrapper: Resetting servo back to degree: %d" % defaultDegree)
 setDegree(0, defaultDegree)
else:
 syslog.syslog(syslog.LOG_NOTICE, "servoWrapper: Setting servo degree to: %d" % userDegree)
 setDegree(0, userDegree)

try:
 client = mqtt.Client()  # create new instance
 client.username_pw_set(mqttUserName, mqttPassword)
 client.connect(mqttBrokerUrlPath, mqttBrokerPort)
 theValueStr = str(userDegree)
 syslog.syslog(syslog.LOG_NOTICE, "servoWrapper: Publishing to home/technical/airCond: %s" % theValueStr)

 client.publish("home/technical/airCond", theValueStr, 0, True)
 client.disconnect()
except:
 syslog.syslog(syslog.LOG_NOTICE, "servoWrapper: Publishing failed.")

syslog.closelog()


