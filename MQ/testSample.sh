#!/usr/bin/env bash

# stop script on error
set -e

# Check to see if root CA file exists, download if not
if false; then
#if [ ! -f ./root-CA.crt ]; then
  printf "\nDownloading AWS IoT Root CA certificate from AWS...\n"
  curl https://www.amazontrust.com/repository/AmazonRootCA1.pem > root-CA.crt
fi

# install AWS Device SDK for Python if not already installed
if false; then
#if [ ! -d ./aws-iot-device-sdk-python ]; then
  printf "\nInstalling AWS SDK...\n"
  git clone https://github.com/aws/aws-iot-device-sdk-python.git
  pushd aws-iot-device-sdk-python
  python setup.py install
  popd
fi

# run pub/sub sample app using certificates downloaded in package
printf "\nRunning pub/sub sample application...\n"
python awsThingPubAsync.py -e a1p6rms6ftf35j-ats.iot.us-east-2.amazonaws.com -r root-CA.crt -c ~/awsCerts/VeePi2.cert.pem -k ~/awsCerts/VeePi2.private.key
