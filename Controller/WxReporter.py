import json
import os
import glob


# Singleton
class WxReporter(object):

    def loadSensorConfigDict(self) :
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

    def assertFoundSensorsEqualConfig(self):
        sensorsPhys = self.listSensors()
        if sensorsPhys == None:
            print("No physical DS W1 sensors found.")
            return None

        sensorsConfig = self.loadSensorConfigDict()['sensorGroup']

        for sensorConfig in sensorsConfig:
            matchedSensor = sensorsPhys.index(sensorConfig['deviceId'])
            if matchedSensor:
                print 'match: ' + matchedSensor

            else:
                print 'Not found: ' + sensorConfig['deviceId']


# dev-time test
reporter = WxReporter()
dict = reporter.listSensors()
print 'physical sensors: '
if dict is not None:
    for entry in dict:
        print entry
else:
    print 'none'
reporter.assertFoundSensorsEqualConfig()
