# mqtt_logger
Transmit log information over MQTT. Designed for use with my Slowloris project.

### How to use
##### External Dependencies
###### Publisher Side
This would be for the Raspberry Pi.
1. [Python 3](https://www.python.org/downloads/) is used for the whole project. The required packages are:
    1. [gzip](https://docs.python.org/3/library/gzip.html) is used to unzip the archives that Apache creates for its 
    logfiles. Part of the Python Standard Library.
    2. [paho-mqtt](https://pypi.org/project/paho-mqtt/) is used to create the MQTT network and send data over it. 
    Install with `pip3 install paho-mqtt`.
    3. [pathlib](https://docs.python.org/3/library/pathlib.html) is used to work with filepaths. 
    Part of the Python Standard Library.
    4. [psutil](https://pypi.org/project/psutil/) is used to collect information on the Raspberry Pi's hardware. 
    Install with `pip3 install psutil`.
2. [Apache2](https://httpd.apache.org/) is used as the webserver. 
It can be installed on Raspberry Pi with `sudo apt-get install apache2 -y`.

###### Subscriber Side
This would be for the main computer. I used my desctop PC running Windows 10.
1. [Python 3](https://www.python.org/downloads/) is used for the whole project. The required packages are:
    2. [paho-mqtt](https://pypi.org/project/paho-mqtt/) is used to create the MQTT network and send data over it. 
    Install with `pip3 install paho-mqtt`.
    3. [pathlib](https://docs.python.org/3/library/pathlib.html) is used to work with filepaths. 
    Part of the Python Standard Library.

##### Run
Once all of those are installed on both machines place `apache_logging.py`, `hardware_logging.py`, and 
`paho_publisher.py` somewhere on the Raspberry Pi. Put `paho_subscriber.py` in your working directory of your main 
computer.


First run the subscriber with `python paho_subscriber.py` then on the Raspberry Pi run the publisher with 
`python publisher.py [seconds to run]` where `[seconds to run]` is an optional argument specifying the length of time to
run for, in seconds. The default is 60 seconds.


##### Results
The subscriber will store all transmitted data in a set of files in the local directory. The file structure is as shown 
below:

        Parent folder > paho_subscriber.py
                        Received Messages > dd-mm-yy hh-mm-ss > subscribed/channel/1
                                                                subscribed/channel/2
                                                                subscribed/channel/3
                                                                ...