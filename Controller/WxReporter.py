import json
import os
import glob

from Sensors.DS18B20.DS18B20Reader import DallasTemptReaderDS18B20
from MQ.pubTempt import Publisher

# from MQ.pubTempt import buildTemptMsg

class WxReporter(object):

    sensorPathPrefix = ''  # /sys/bus/w1/devices/
    sensorPathRoot = ''    # 28*
    sensorPathSuffix = ''  # /w1_slave
    availableSensorIdList = []
    unavailableSensorIdList = []
    availableSensorName2DeviceDict = {}  # turtleTank : /sys/bus/w1/devices/28-02039246ae40/w1_slave

    sensorName2DeviceIdDict = {}

    def loadConfigVals(self):
        config = self.loadSensorConfigDict()
        self.sensorPathPrefix = config['pathParts']['prefix']  # todo:bug: if the prefix is not found, then the not-found bucket will be empty. Instead, it should have all the sensors for the json, as none will be found
        self.sensorPathRoot = config['pathParts']['root']
        self.sensorPathSuffix = config['pathParts']['suffix']

    def loadSensorConfigDict(self):
        print 'config path: ' + os.getcwd() + ' file hard-coded as sensor-config.json'
        with open('sensor-config.json') as config_file:
            return json.load(config_file)

    # return list of sensors found in OS (no consider config file)
    def listSensors(self, devicePath ="/sys/bus/w1/devices/", w1Prefix = "28*"):

        # enable kernel modules
        os.system('sudo modprobe w1-gpio')
        os.system('sudo modprobe w1-therm')

        # search for a device file that starts with 28
        # ex: '/sys/bus/w1/devices/28*'
        endpoint = devicePath + w1Prefix
        devicelist = glob.glob(endpoint)
        if devicelist == '' or len(devicelist) < 1:
            return None
        else:
            return devicelist

    # Convert list of found sensors into dictionary, with key that of the json file definition
    # Drop sensors that are not in config file
    def dictSensors(self):
        sensordict = {}
        sensorlist = self.listSensors(self.sensorPathPrefix, self.sensorPathRoot)

        if sensorlist is None: return None

        name = ''
        parts = []

        for path in sensorlist:
            parts = path.split("/")
            sensordict[parts[len(parts)-1]] = path

        return sensordict

    def populateFoundList(self):

        sensorsPhys = self.dictSensors()
        if sensorsPhys is None:
            print("No physical DS W1 sensors found.")
            return None

        sensorsConfig = self.loadSensorConfigDict()['sensorGroup']

        for sensorConfig in sensorsConfig:
            uConfigId = sensorConfig['deviceId']
            configId = uConfigId.encode('ascii','ignore')  # removes the u from unicode prefix

            uConfigName = sensorConfig['sensorName']
            configName = uConfigName.encode('ascii','ignore')

            try:
                matchedSensor = sensorsPhys[configId]
                self.availableSensorIdList.append(configId)
                self.availableSensorName2DeviceDict[configName] = str(str(matchedSensor) + self.sensorPathSuffix).encode('ascii','ignore')

            except   KeyError:
                self.unavailableSensorIdList.append(configId)

    def readTemperature(self, sensorName):
        device = self.availableSensorName2DeviceDict[sensorName]
        reader = DallasTemptReaderDS18B20(device)
        tempt = reader.readDeviceTempt()
        print "WxReporter SensorName[" + sensorName + "] celcius: " + str(tempt)
        return tempt

    def publishValue(self, jsonPayload, publisher):
        # publisher = Publisher('srlAwsConfig.ini')
        publisher.publish(jsonPayload)

    def __init__(self):
        print 'config path: ' + os.getcwd()
        self.loadConfigVals()



def main():
    reporter = WxReporter()

    reporter.populateFoundList()
    print "Found availableSensorIdList " + str(reporter.availableSensorIdList)
    print "Found availableSensorName2DeviceDict " + str(reporter.availableSensorName2DeviceDict)
    print "NOT found" + str(reporter.unavailableSensorIdList)

    print "\nLooping found sensors..."
    for sensor in reporter.availableSensorName2DeviceDict:
        tempt = reporter.readTemperature(sensor)
        print "\nreturn val " + str(tempt) + "\n"
        publisher = Publisher('../srlAwsConfig.ini')
        msg = publisher.buildTemptMsg(sensor, tempt, 'C')
        reporter.publishValue(msg, publisher)


if __name__ == "__main__":
    main()
