from datetime import datetime
from pathlib import Path

import paho.mqtt.client as mqtt

master_topic_list = "topics"

# make new folder for messages
dt = str(datetime.now()).split('.')[0]
dt = dt.replace(':', '-')
cwd = str(Path.cwd())
msg_folder = str(Path("/Received Messages"))
received = Path(cwd + msg_folder + '/' + dt)
received.mkdir(parents=True, exist_ok=True)


def write_data(message):
	filename = str(message.topic).replace('/', '-') + '.txt'
	msg = message.payload.decode("utf-8") + '\n'
	with open(received / filename, 'a') as f:
		f.write(msg)
	f.close()


def on_message(client, obj, message):
	print("Message from '" + message.topic + "':\t" + str(message.payload.decode("utf-8")))

	if message.topic == master_topic_list:
		new_topic = message.payload.decode("utf-8")
		client.subscribe(new_topic)
	else:
		write_data(message)


def on_subscribe(client, obj, message):
	print("Subscribing to: " + message)


def main():
	mqtt_server = "localhost"

	print("Creating new instance...")
	client = mqtt.Client("Subscriber1")
	client.on_message = on_message
	client.on_subscribe = on_subscribe
	print("Connecting to broker...")
	client.connect(mqtt_server)
	client.subscribe(master_topic_list)
	client.loop_forever()


if __name__ == '__main__':
	main()
