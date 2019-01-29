import logging
import time
import json
from pubTempt import Publisher


# Configure logging
logger = logging.getLogger("pubTemptTest")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

publisher = Publisher()

# Publish to the same topic in a loop forever
loopCount = 0
while loopCount < 1 :
    message = {}
    message['thingName'] = 'sampleThing'
    # message['timestamp'] = loopCount
    # message['sensorTime'] = str(time.clock())
    message['sensorTime'] = str(time.time())
    messageJson = json.dumps(message)

    # publisher.publish(messageJson) Why did the sample work but for real data, i must .loads as below?
    publisher.publish(json.loads(messageJson))

    loopCount += 1
    time.sleep(1)

    # Jan 2019
    #todo:workingHere: pull in key config from json config file
    # then write to topic
    # then run this every 10 mins to update tempt to topic

    # 1. create setter for tempt message that accetps timestamp and temp and location and topic
