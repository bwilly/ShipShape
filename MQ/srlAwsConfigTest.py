import ConfigParser

config = ConfigParser.ConfigParser()
config.read('srlAwsConfig.ini')

privateKey = config.get('DEFAULT','PRIVATE_KEY_FILE')
publicKey = config.get('DEFAULT','PUBLIC_KEY_FILE')
cert = config.get('DEFAULT','CERT_FILE')

print privateKey
