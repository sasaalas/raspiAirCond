import argparse
import paho.mqtt.client as mqtt
import time
import signal
import subprocess
import threading


loop_flag = 1
fail_count = 0
user_exit = False

servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
max_degree = 60  # Degrees your servo can rotate
default_degree = 30
mqttUserName = "your-broker-username-here"
mqttPassword = "your-broker-password-here"

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default
    
def main(brokerUrl, brokerPort):
    print('Starting...')        

parser = argparse.ArgumentParser(description='main')
parser.add_argument('--brokerUrl', required=True, type=str)
parser.add_argument('--brokerPort', required=True, type=str)
args = parser.parse_args()
brokerUrl = args.brokerUrl
brokerPort = args.brokerPort

main(brokerUrl, brokerPort)
