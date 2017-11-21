import json


def fahrenheit_to_celsius(x):
    """Convert degrees in fahrenheit to celsius"""
    return (x - 32) * 0.5556


class THSensor:
    def __init__(self, config, data):
        self.data = data
        self.rooms = {int(k): v for k, v in config['channel_to_location'].items()}
        self.topics = config['output_topics']

    def get_all_topics(self):
        all_topics = []
        for room in self.rooms.values():
            for topic in self.topics:
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
