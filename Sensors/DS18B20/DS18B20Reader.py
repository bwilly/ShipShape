# Singleton
class DallasTemptReaderDS18B20(object):

    devicefile = ''

    # get temerature
    # returns None on error, or the temperature as a float
    def readDeviceTempt(self):
        try:
            fileobj = open(self.devicefile, 'r')
            lines = fileobj.readlines()
            fileobj.close()
        except:
            print 'EXCEPTION on fileobj open'
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
            print "tempt C: " + str(tempvalue)
            print "\r"
            return tempvalue
        else:
            print "There was an error in the read content. Status: " + str(status)
            print lines
            print "\r"
            return None

    def __init__(self, devicefile):
        self.devicefile = devicefile
