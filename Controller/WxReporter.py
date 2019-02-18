import json
import os
import glob

from Sensors.DS18B20.DS18B20Reader import DallasTemptReaderDS18B20


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
        print "WxReporter SensorName[" + sensorName + "] celcius: " + str(reader.readDeviceTempt())

    # workingHere
    # def publishValue(self, payload):
    #     publisher = Publisher()
    #
    def __init__(self):
        self.loadConfigVals()


# dev-time test
reporter = WxReporter()
# dict = reporter.listSensors()
# print 'physical sensors: '
# if dict is not None:
#     for entry in dict:
#         print entry
# else:
#     print 'none'
reporter.populateFoundList()
print "Found " + str(reporter.availableSensorIdList)
print "Found " + str(reporter.availableSensorName2DeviceDict)
print "NOT found" + str(reporter.unavailableSensorIdList)

print "\nLooping found sensors..."
for sensor in reporter.availableSensorName2DeviceDict:
    reporter.readTemperature(sensor)
