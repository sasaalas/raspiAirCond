import argparse
import paho.mqtt.client as mqtt
import threading
import signal
import time
import sys, os.path
servo_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/pwmServoDriver/')
sys.path.append(servo_dir)
from Raspi_PWM_Servo_Driver import PWM

loop_flag = 1
user_exit = False

servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
max_degree = 60  # Degrees your servo can rotate

mqttUserName = "your-broker-username-here"
mqttPassword = "your-broker-password-here"

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

class SummingThread(threading.Thread):
     def __init__(self,sleeptime,finaldegree):
         super(SummingThread, self).__init__()
         self.sleeptime=sleeptime         
         self.finaldegree=finaldegree

     def run(self):
         time.sleep(self.sleeptime)
         user_degree = self.finaldegree         
         set_degree(0, user_degree)

def set_degree(channel, d):
    print("mqttListener: Setting servo degree to: %d" % d)            
    degree_pulse = servo_min
    degree_pulse += int((servo_max - servo_min) / max_degree) * d
    pwm.setPWM(channel, 0, degree_pulse)
    

def set_timed_degree(channel, d, sleeptime):
    print("mqttListener: Setting timer for setting servo degree.")
    set_degree(channel, d)
    sleeptime = 300
    finaldegree = 30    
    thread1 = SummingThread(sleeptime, finaldegree)
    thread1.start()     

def perform_heating(param1):
    print("mqttListener: Heating function not implemented")

def perform_air_cond(param1):
    user_degree = 0
    if param1 == 1:
        user_degree = 0
    elif param1 == 2:
        user_degree = 30
    elif param1 == 3:
        user_degree = 60
    elif param1 == 4:
        user_degree = 60
        sleeptime = 60
        set_timed_degree(0, user_degree, sleeptime)
        return
    
    set_degree(0, user_degree)

def on_message(client, userdata, message):
    print("mqttListener: Message received ", str(message.payload.decode("utf-8")))
    print("mqttListener: Message topic=", message.topic)
    print("mqttListener: Message qos=", message.qos)
    print("mqttListener: Message retain flag=", message.retain)

    the_int_string = message.payload.decode("utf-8")
    the_int = safe_cast(message.payload, int)  # will return None
    if the_int is None:
        print("mqttListener: Payload is None. Returning.")
        return

    if message.retain == 1:
        print("mqttListener: Message retain is 1. Returning.")
        return

    if message.topic == "home/technical/setHeating":        
        perform_heating(the_int)        
    elif message.topic == "home/technical/setAirCond":
        perform_air_cond(the_int)
        the_topic = "home/technical/airCond"
        client.publish(the_topic, the_int, 0, True)
    else:
        print("mqttListener: Received unknown topic.")

def on_handlesignal(param1, param2):
    global user_exit
    print("mqttListener: Received on_handlesignal.")
    user_exit = True
    global loop_flag
    loop_flag = 0    

def on_connect(client, userdata, flags, rc):
    print("mqttListener: Received on_connect.")

def on_disconnect(client, userdata,rc=0):
    global loop_flag
    print("mqttListener: Received on_disconnect.")
    loop_flag = 0
    
    if user_exit == True:
      print("mqttListener: Received user exit. Returning.")
      return        

def performConnect():
    client = mqtt.Client()  # create new instance
    client.on_disconnect = on_disconnect
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(mqttUserName, mqttPassword)
    
    theIntPort = safe_cast(brokerPort, int)
    if theIntPort is None:
        print("mqttListener: Invalid brokerPort. Returning.")
        return
        
    client.connect(brokerUrl, theIntPort)
    
    the_topic1 = "home/technical/setAirCond"
    client.subscribe(the_topic1)

    the_topic2 = "home/technical/setHeating"
    client.subscribe(the_topic2)  
    return client
    
def main(brokerUrl, brokerPort):  
    signal.signal(signal.SIGINT, on_handlesignal)
    signal.signal(signal.SIGTERM, on_handlesignal)

    client = performConnect()
    client.loop_start()  # start the loop  

    while loop_flag == 1:
        time.sleep(1)

    client.disconnect()
    client.loop_stop()

parser = argparse.ArgumentParser(description='main')
parser.add_argument('--brokerUrl', required=True, type=str)
parser.add_argument('--brokerPort', required=True, type=str)
args = parser.parse_args()
brokerUrl = args.brokerUrl
brokerPort = args.brokerPort

# Initialise the PWM device using the default address
pwm = PWM(0x6F, debug=False)
pwm.setPWMFreq(60)  # Set PWM frequency to 60Hz

main(brokerUrl, brokerPort)
