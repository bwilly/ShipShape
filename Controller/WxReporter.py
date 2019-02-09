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
        physSensors = self.listSensors()
        if physSensors == None:
            print("No physical DS W1 sensors found.")
            return None

        for sensor in self.loadSensorConfigDict()['sensorGroup']:
            sensorId = sensor['deviceId']
            if(physSensors[sensorId]): print("found " + sensorId)
            else: print("NOT found " + sensorId)



# dev-time test
reporter = WxReporter()
dict = reporter.listSensors()
print(dict)
reporter.assertFoundSensorsEqualConfig()
