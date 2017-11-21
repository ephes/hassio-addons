import sys
import json
import paho.mqtt.client as mqtt

from sensors import THSensor


def on_connect(client, userdata, flags, rc):
    client.subscribe(client.config['input_topic'])


def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    if data.get('model', '') == 'Ambient Weather F007TH Thermo-Hygrometer':
        thsensor = THSensor(client.config, data)
        for topic, payload in thsensor.new_messages():
            client.publish(topic, payload=payload, qos=0, retain=True)

with open(sys.argv[1]) as f:
    config = json.load(f)

client = mqtt.Client()
client.config = config
client.on_connect = on_connect
client.on_message = on_message

username, password = config.get('mqtt_user', ''), config.get('mqtt_password', '')
if len(username) > 0:
    if len(password) > 0:
        client.username_pw_set(username, password=password)
    else:
        client.username_pw_set(username)
client.connect(config.get('mqtt_host', 'hassio.local'))
client.loop_forever()
