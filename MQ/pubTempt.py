'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the Licens5e.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import ConfigParser

AllowedActions = ['both', 'publish', 'subscribe']

class Publisher:

    # Custom MQTT message callback
    def customCallback(client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

    @property
    def msg(self):
        return self.__msg

    @msg.setter
    def msg(self, msg):
        self.__msg = msg

    # Read in command-line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False, help="Use MQTT over WebSocket")
    #parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")
    # parser.add_argument("-m", "--mode", action="store", dest="mode", default="both", help="Operation modes: %s"%str(AllowedActions))
    parser.add_argument("-m", "--mode", action="store", dest="mode", default="publish", help="Operation modes: %s"%str(AllowedActions))
    #parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!", help="Message to publish")

    # Jan19 -- args aren't or shouldn't be used anymore.
    args = parser.parse_args()
    # port = args.port
    useWebsocket = args.useWebsocket


    # config
    config = ConfigParser.ConfigParser()
    config.read('srlAwsConfig.ini')

    privateKeyPath = config.get('DEFAULT','PRIVATE_KEY_FILE')
    # publicKeyPath = config.get('DEFAULT','PUBLIC_KEY_FILE')
    certificatePath = config.get('DEFAULT','CERT_FILE')
    rootCAPath = config.get('DEFAULT',"ROOT_CA")
    topic = config.get('DEFAULT',"TOPIC")
    host = config.get('DEFAULT',"ENDPOINT")

    # test
    # _message = "testMsg"
    _message = msg

    if args.mode not in AllowedActions:
        parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
        exit(2)

    if args.useWebsocket and args.certificatePath and args.privateKeyPath:
        parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
        exit(2)

    if not args.useWebsocket and not privateKeyPath:
        parser.error("Missing credentials for authentication." + privateKeyPath)
        exit(2)

    # Port defaults
    if args.useWebsocket:  # When no port override for WebSocket, default to 443
        port = 443
    if not args.useWebsocket:  # When no port override for non-WebSocket, default to 8883
        port = 8883

    # Configure logging
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.ERROR)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    clientId = 'testClient'  # + str(time.clock()) # if same name then cxn prob possible if reused before recycled |bwilly

    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient = None
    if useWebsocket:
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
        myAWSIoTMQTTClient.configureEndpoint(host, port)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath)
    else:
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
        myAWSIoTMQTTClient.configureEndpoint(host, port)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    def publish(self, msg):
        # Connect and subscribe to AWS IoT
        self.myAWSIoTMQTTClient.connect()
        #if args.mode == 'both' or args.mode == 'subscribe':
        # self.myAWSIoTMQTTClient.subscribe(self.topic, 1, self.customCallback)
        time.sleep(2)

        if self.args.mode == 'both' or self.args.mode == 'publish':
            message = {}
            message['message'] = msg
            messageJson = json.dumps(message)
            self.myAWSIoTMQTTClient.publishAsync(self.topic, messageJson, 1)  # was sync
            print('Published topic %s: %s\n' % (self.topic, messageJson))

        self.myAWSIoTMQTTClient.disconnect()


        # Jan 2019
        #todo:workingHere: pull in key config from json config file
        # then write to topic
        # then run this every 10 mins to update tempt to topic

        # 1. create setter for tempt message that accetps timestamp and temp and location and topic
