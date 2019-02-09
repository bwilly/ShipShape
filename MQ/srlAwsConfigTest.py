import ConfigParser

configIni = ConfigParser.ConfigParser()
configIni.read('srlAwsConfig.ini')

privateKey = configIni.get('DEFAULT', 'PRIVATE_KEY_FILE')
publicKey = configIni.get('DEFAULT', 'PUBLIC_KEY_FILE')
cert = configIni.get('DEFAULT', 'CERT_FILE')

print privateKey
