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

import os

AllowedActions = ['both', 'publish', 'subscribe']


#  todo: this feels very scripty
class Publisher(object):

    _iniConfigPath = "not yet set"
    _privateKeyPath = "not yet set"
    _rootCAPath = "not yet set"
    _host = "not yet set"
    _certificatePath = "not yet set"

    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient = None

    def __init__(self, iniConfigPath):
        print 'AWS IoT Config file: ' + iniConfigPath + ' for: ' + __file__
        self._iniConfigPath = iniConfigPath
        self.initConfig()

        self.prepareClient()


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
    _useWebsocket = args.useWebsocket


    def initConfig(self):
        # config
        print "pubTempt loading config file: " + self._iniConfigPath
        config = ConfigParser.ConfigParser()

        config.read(self._iniConfigPath)
        # config.read('../MQ/srlAwsConfig.ini')
        # config.read('MQ/srlAwsConfig.ini')

        try:
            if len(config.defaults()) < 1:
                raise BaseException('Could not locate AWS IoT config at: ' + self._iniConfigPath)
            print config.defaults()
        except BaseException as e:
            print e
            print 'CWD: ' + os.getcwd()


        basePath = config.get('DEFAULT','KEY_PATH')

        self._privateKeyPath = basePath + config.get('DEFAULT','PRIVATE_KEY_FILE')
        # publicKeyPath = config.get('DEFAULT','PUBLIC_KEY_FILE')
        self._certificatePath = basePath + config.get('DEFAULT','CERT_FILE')
        self._rootCAPath = basePath + config.get('DEFAULT',"ROOT_CA")
        self._topic = config.get('DEFAULT',"TOPIC")
        self._host = config.get('DEFAULT',"ENDPOINT")

    # test
    # _message = "testMsg"
    _message = msg

    if args.mode not in AllowedActions:
        parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
        exit(2)

    if args.useWebsocket and args.certificatePath and args.privateKeyPath:
        parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
        exit(2)

    if not args.useWebsocket and not _privateKeyPath:
        parser.error("Missing credentials for authentication." + _privateKeyPath)
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

    _clientId = 'testClient'  # + str(time.clock()) # if same name then cxn prob possible if reused before recycled |bwilly



    def prepareClient(self):

        if self._useWebsocket:
            myAWSIoTMQTTClient = AWSIoTMQTTClient(self._clientId, self._useWebsocket)
            myAWSIoTMQTTClient.configureEndpoint(self._host, self._port)
            myAWSIoTMQTTClient.configureCredentials(self._rootCAPath)
        else:
            myAWSIoTMQTTClient = AWSIoTMQTTClient(self._clientId)
            myAWSIoTMQTTClient.configureEndpoint(self._host, self.port)
            myAWSIoTMQTTClient.configureCredentials(self._rootCAPath, self._privateKeyPath, self._certificatePath)

        # AWSIoTMQTTClient connection configuration
        myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        self.myAWSIoTMQTTClient = myAWSIoTMQTTClient

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
            self.myAWSIoTMQTTClient.publishAsync(self._topic, messageJson, 1)  # was sync
            print('Published topic %s: %s\n' % (self._topic, messageJson))

        self.myAWSIoTMQTTClient.disconnect()

        # Jan 2019
        # todo:workingHere: pull in key config from json config file
        # then write to topic
        # then run this every 10 mins to update tempt to topic

        # 1. create setter for tempt message that accetps timestamp and temp and location and topic

    # todo: move this method outside of publish class, as class should know nothing about how to build msg. tried as jsut a def outisde class, but compilter/runner fialed with from AWSIoTPythonSDK.core.util.providers import CertificateCredentialsProvider \n ImportError: No module named AWSIoTPythonSDK.core.util.providers
    #  Message (during dev/test) to Published topic test/sensor/wx:
    #  {"message": {"sensorTimePretty": "['Sun Feb 19']", "thingName": "sampleThing", "sensorTime": "1550462372.49"}}
    # returns msg as string
    def buildTemptMsg(self, sensorName, temperature, unit):

        message = {}

        message['thingName'] = 'sampleThing'
        message['sensorName'] = sensorName
        message['tempt'] = temperature
        message['unit'] = unit
        message['sensorTime'] = str(time.time())
        days = [time.strftime("%a %b %y")]
        message['sensorTimePretty'] = str(days)
        messageJson = json.dumps(message)

        return messageJson

