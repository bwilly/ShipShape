import json
import os
import glob


# Singleton
class WxReporter(object):

    sensorPathPrefix = ''  # /sys/bus/w1/devices/
    sensorPathRoot = ''    # 28*
    availableSensorIdList = []
    unavailableSensorIdList = []

    def loadConfigVals(self):
        config = self.loadSensorConfigDict()
        self.sensorPathPrefix = config['pathParts']['prefix']
        self.sensorPathRoot = config['pathParts']['root']

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

    def assertFoundSensorsEqualConfig(self):

        sensorsPhys = self.dictSensors()
        if sensorsPhys is None:
            print("No physical DS W1 sensors found.")
            return None

        sensorsConfig = self.loadSensorConfigDict()['sensorGroup']

        for sensorConfig in sensorsConfig:
            uConfigId = sensorConfig['deviceId']
            configId = uConfigId.encode('ascii','ignore')
            try:
                matchedSensor = sensorsPhys[configId]
                self.availableSensorIdList.append(configId)

            except:
                self.unavailableSensorIdList.append(configId)
                

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
reporter.assertFoundSensorsEqualConfig()
print "Found " + str(reporter.availableSensorIdList)
print "NOT found" + str(reporter.unavailableSensorIdList)
