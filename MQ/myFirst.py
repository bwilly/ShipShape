
import logging
import time
import argparse
import json

# todo: scrap that file. I don't even know if it works.
#  has been superceeed by pubTemptTest and pubTempt


AllowedActions = ['both', 'publish', 'subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


port = 8883

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Publish to the same topic in a loop forever
loopCount = 0
while True:

    message = {}
    message['message'] = args.message
    message['sequence'] = loopCount
    messageJson = json.dumps(message)

    print('Published topic %s: %s\n' % ("test/sensor/wx", messageJson))
    loopCount += 1
    time.sleep(1)

    #todo:workingHere: pull in key config from json config file
    # then write to topic
    # then run this every 10 mins to update tempt to topic
