# raspiAirCond
Tested with Raspbian GNU/Linux 9 (stretch) and Raspbian GNU/Linux 10 (buster)

Preconditions:
1. There is MQTT broker available. In this example RabbitMQ with MQTT -plugin is running at 192.168.0.2/1883. MQTT -username and -password must be set in mqttHomeListener.py.
2. I2C is enabled. This can be done using Raspberry Pi Configuration -utility.

Running:
1. pip3 install smbus2 paho-mqtt
2. python3 mqttHomeListener.py --brokerUrl 192.168.0.2 --brokerPort 1883
