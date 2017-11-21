import sys
import json
import paho.mqtt.client as mqtt


def fahrenheit_to_celsius(x):
    """Convert degrees in fahrenheit to celsius"""
    return (x - 32) * 0.5556


class THSensor:
    def __init__(self, config, data):
        self.data = data
        self.rooms = {int(k): v for k, v in config['rooms'].items()}
        self.topics = config['output_topics']

    @classmethod
    def get_all_topics(cls):
        all_topics = []
        for room in cls.rooms.values():
            for topic in cls.topics:
                all_topics.append('/homeassistant/{}/{}'.format(room, topic))
        return all_topics

    @property
    def topic_tmpl(self):
        return '/homeassistant/{}/{{}}'.format(self.rooms[self.data['channel']])

    @property
    def temperature(self):
        topic = self.topic_tmpl.format('temperature')
        payload = json.dumps(
            {'temperature': fahrenheit_to_celsius(self.data['temperature_F'])})
        return topic, payload

    @property
    def humidity(self):
        topic = self.topic_tmpl.format('humidity')
        payload = json.dumps({'humidity': self.data['humidity']})
        return topic, payload

    @property
    def battery(self):
        topic = self.topic_tmpl.format('battery')
        payload = json.dumps({'battery': self.data['battery']})
        return topic, payload

    def new_messages(self):
        messages = []
        for topic in self.topics:
            messages.append(getattr(self, topic))
        return messages


def on_connect(client, userdata, flags, rc):
    client.subscribe(client.config['input_topic'])
    for topic in THSensor.get_all_topics():
        client.subscribe(topic)


def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    if data.get('model', '') == 'Ambient Weather F007TH Thermo-Hygrometer' and False:
        thsensor = THSensor(client.config, data)
        for topic, payload in thsensor.new_messages():
            client.publish(topic, payload=payload, qos=0, retain=True)

with open(sys.argv[1]) as f:
    config = json.load(f)['options']
print(config)

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
