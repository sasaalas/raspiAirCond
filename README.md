DISCLAIMER:
Code in pwmServoDriver -folder is slightly modified version of original code which can be found from various sources from Internet. I do not know who is the original author.

# raspiAirCond
Tested with Raspbian Stretch (Python 3.5.3) and with Raspbian Buster (Python 3.7.3)

Preconditions:
1. There is MQTT broker available (see wiki). In this example RabbitMQ with MQTT -plugin is running at 192.168.0.2/1883. MQTT -username and -password must be set in mqttHomeListener.py.
2. I2C is enabled. This can be done using Raspberry Pi Configuration -utility.

1. Running mqttHomeListener
1.1 pip3 install smbus2 paho-mqtt
1.2 python3 mqttHomeListener.py --brokerUrl 192.168.0.2 --brokerPort 1883

2. Running restAPI
2.1 npm install
2.2 node bin/www
