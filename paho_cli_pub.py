# Finlay Miller 2019
# Raspberry Pi hardware data logging script
# Communication Networks Term Project
#
# Uses psutil to gather all hardware data relevant to monitoring my Raspberry Pi Zero W
# To be used with the rest of my MQTT logging scripts.

import sys
import time
from pathlib import Path

import paho.mqtt.publish as publish

import apache_logging as al
import hardware_logging as hl


def get_paths(input_dict):
	"""
	Get paths from dictionary. get_hardware_data() returns nested dicts. This function converts the keys of the nested
	dicts to filepath-type strings which will later be used as MQTT broadcast channels.

	:param input_dict: Dictionary to be worked on
	:return: generator of paths
	"""
	for key, value in input_dict.items():
		if isinstance(value, dict):
			for subkey in get_paths(value):
				yield key + '/' + subkey
		else:
			yield key


def get_vals(input_dict):
	for key, value in input_dict.items():
		if isinstance(value, dict):
			yield from get_vals(value)
		else:
			yield value


def main(argv):
	mqtt_server = "localhost"
	mqtt_apache_access = "apache/access"
	mqtt_apache_error = "apache/error"

	# set up length of time to log data for
	if argv:
		time_to_run = argv
	else:
		time_to_run = 30

	# broadcast list of channels for subscriber to listen to
	hardware_data = hl.get_hw_data()
	for path in get_paths(hardware_data):
		publish.single("topics", path, hostname=mqtt_server)
	publish.single("topics", mqtt_apache_access, hostname=mqtt_server)
	publish.single("topics", mqtt_apache_error, hostname=mqtt_server)
	# give subscribers a chance to subscribe
	time.sleep(2)

	# log and broadcast hardware data for set length of time
	t0 = time.time()
	while True:
		t1 = time.time()
		hardware_data = hl.get_hw_data()

		for path, val in zip(get_paths(hardware_data), get_vals(hardware_data)):
			publish.single(path, str(val), hostname=mqtt_server)

		if (t1 - t0) > time_to_run:
			break
		time.sleep(1)

	# log and broadcast Apache data. Apache automatically writes all the
	# information we need to files so we don't need to run it in the loop.

	# uncomment lines below depending on workspace
	# filepath   = Path("/var/log/apache2")                                                      # raspberry pi
	# filepath   = Path("C:/Users/minla/OneDrive/Documents/Raspberry Pi/Apache Logs")            # surface
	filepath = Path("C:/Users/Finlay Miller/OneDrive/Documents/Raspberry Pi/Apache Logs")  # desktop

	apache_data = al.get_ap_data("access.*", filepath)
	publish.single(mqtt_apache_access, str(apache_data), hostname=mqtt_server)
	apache_data = al.get_ap_data("error.*", filepath)
	publish.single(mqtt_apache_error, str(apache_data), hostname=mqtt_server)


if __name__ == '__main__':
	main(sys.argv[1:])
