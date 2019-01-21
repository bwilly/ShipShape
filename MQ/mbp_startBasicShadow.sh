# Jan20-19
# This works local on MBP and I can see shadow updating at AWS. But I don't want to have to start it from a script.
# And I want the keys to be ref'd by config file.
# But this must be run possibly on first install for each pi, as it d/l the root cert. See below.

# stop script on error
set -e

# Check to see if root CA file exists, download if not
if [ ! -f ./root-CA.crt ]; then
  printf "\nDownloading AWS IoT Root CA certificate from AWS...\n"
  curl https://www.amazontrust.com/repository/AmazonRootCA1.pem > root-CA.crt
fi

# install AWS Device SDK for Python if not already installed
if [ ! -d ./aws-iot-device-sdk-python ]; then
  printf "\nInstalling AWS SDK...\n"
  git clone https://github.com/aws/aws-iot-device-sdk-python.git
  pushd aws-iot-device-sdk-python
  python setup.py install
  popd
fi

# run pub/sub sample app using certificates downloaded in package
printf "\nRunning pub/sub sample application...\n"
python basicShadowUpdater.py -n Mbp2016 -e a1p6rms6ftf35j-ats.iot.us-east-2.amazonaws.com -r root-CA.crt -c Mbp2016.cert.pem -k Mbp2016.private.key
