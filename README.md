# ShipShape

targeting RasPi, Python and Temperature Sensors

Feb18-20
Abandoning in favor of Node. Starting from scratch. For the following reasons:
I remember this code from last year, but it doesn't do much more than write simple sample messages to Thing Shadow.
It does not seem to publish temperature yet.

Feb17-20
Tests:
cd /Users/bwilly/Projects/Projects/YachtMonitor2019/ShipShapePi/MQ
./mbp_testSample.sh
python awsThingPubAsync.py
[not sure where to see results for this]

./mbp_startBasicShadow.sh
python basicShadowUpdater.py -n Mbp2016
[go here to see results: https://us-east-2.console.aws.amazon.com/iot/home?region=us-east-2#/thing/Mbp2016]

@see evernote: AWS IoT Python / PIP Setup Mac, https://www.evernote.com/l/AEhON7fCsDFIRKtjdoYkuZOKtqDQb8WAMP4

===========

Dec24-19: this is from last spring, so I am guessing, but i think that I prob stopped
dev on this while I figured out local AWS Dynamo. I am not done yet w/ local.
Presumably, I'd then know dynamo and get back to MQ on AWS (serverless, was it?) to write to AWS Dynamo (non local)

Actually, @see evernote:ShipShapeAwsApi, https://www.evernote.com/l/AEgAIpILuoZAOLpKMJtVH9Gjzh_UnmSHRqQ, which currently reads:
April 21, 2019

I believe I installed aws-iot-device-sdk in error.
As I will not right now be using this to connect right away to MQTT.
Instead, I will connect node to Dynamo to get data
. TheMQTT sdk I expect to use someday to replace the python writer to the IoT shadow.
