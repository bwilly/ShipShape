import ConfigParser
import sys


configIni = ConfigParser.ConfigParser()
configIni.read('srlAwsConfig.ini')


debugConfigInfo = configIni.get('DEFAULT', 'THIS_INI_ID')
privateKey = configIni.get('DEFAULT', 'PRIVATE_KEY_FILE')
publicKey = configIni.get('DEFAULT', 'PUBLIC_KEY_FILE')
cert = configIni.get('DEFAULT', 'CERT_FILE')

print debugConfigInfo

