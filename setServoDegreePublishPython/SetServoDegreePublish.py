#!/usr/bin/env python

from Raspi_PWM_Servo_Driver import PWM
import sys
import time
import syslog
import sys
import paho.mqtt.client as mqtt

syslog.openlog(sys.argv[0])
 
# Get the total number of args passed to the demo.py
total = len(sys.argv)

if (total != 3):
 print ("Incorrect parameters");
 syslog.closelog()
 sys.exit()

userDegree = int(sys.argv[1])
userTime = int(sys.argv[2])
brokerUrlPath = "your-broker-url-here"
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
 syslog.syslog(syslog.LOG_NOTICE, "Setting servo degree to: %d" % userDegree)
 setDegree(0, userDegree)
 syslog.syslog(syslog.LOG_NOTICE, "Sleeping: %d" % userTime)
 time.sleep(userTime)
 syslog.syslog(syslog.LOG_NOTICE, "Resetting servo back to degree: %d" % defaultDegree)
 setDegree(0, defaultDegree)
else:
 syslog.syslog(syslog.LOG_NOTICE, "Setting servo degree to: %d" % userDegree)
 setDegree(0, userDegree)

try:
 client = mqtt.Client()  # create new instance
 client.username_pw_set(mqttUserName, mqttPassword)
 client.connect(brokerUrlPath, 12676)
 theValueStr = str(userDegree)
 syslog.syslog(syslog.LOG_NOTICE, "Publishing to home/technical/airCond: %s" % theValueStr)

 client.publish("home/technical/airCond", theValueStr, 0, True)
 client.disconnect()
except:
 syslog.syslog(syslog.LOG_NOTICE, "Publishing failed")

syslog.closelog()


