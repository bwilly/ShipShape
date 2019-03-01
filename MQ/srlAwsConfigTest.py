import ConfigParser
import sys
import os



configIniPath = 'config/srlAwsConfig-test.ini' # python cwd relative to this value

configIni = ConfigParser.ConfigParser()
configIni.read(configIniPath)

if len(configIni.defaults()) < 1:
    raise BaseException('Could not locate AWS IoT config at: ' + configIniPath + '. Expected CWD of Python to be local to: ' + os.path.dirname(os.path.abspath( __file__ )))
print configIni.defaults()



debugConfigInfo = configIni.get('DEFAULT', 'THIS_INI_ID')
privateKey = configIni.get('DEFAULT', 'PRIVATE_KEY_FILE')
publicKey = configIni.get('DEFAULT', 'PUBLIC_KEY_FILE')
cert = configIni.get('DEFAULT', 'CERT_FILE')

print 'THIS_INI_ID: ' + debugConfigInfo

