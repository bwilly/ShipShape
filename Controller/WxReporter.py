import json
import os
import glob


# Singleton
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
        self.sensorPathPrefix = config['pathParts']['prefix']
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
                self.availableSensorName2DeviceDict[configName] = str(matchedSensor) + self.sensorPathSuffix

            except   KeyError:
                self.unavailableSensorIdList.append(configId)

    def readTemperature(self, sensorName):

        reader = DallasTemptReaderDS18B20()

    def __init__(self):
        self.loadConfigVals()


class DallasTemptReaderDS18B20(object):

    devicefile = ''

    # get temerature
    # returns None on error, or the temperature as a float
    def readDeviceTempt(self, devicefile):
        try:
            fileobj = open(devicefile, 'r')
            lines = fileobj.readlines()
            fileobj.close()
        except:
            print 'exception on fileobj open'
            return None

        # get the status from the end of line 1
        status = lines[0][-4:-1]

        # is the status is ok, get the temperature from line 2
        if status == "YES":
            print status
            rawline = lines[1]  # lines[1][-6:-1]
            tempstartindex = rawline.find("=") + 1
            tempstr = rawline[tempstartindex:-1]
            print "tempstr: " + tempstr
            tempvalue = float(tempstr) / 1000
            print tempvalue
            return tempvalue
        else:
            print "There was an error."
            return None

    def __init__(self, devicefile):
        self.devicefile = devicefile


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
