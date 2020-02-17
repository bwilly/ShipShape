# ShipShape

targeting RasPi, Python and Temperature Sensors

Feb17-19
Tests:
cd /Users/bwilly/Projects/Projects/YachtMonitor2019/ShipShapePi/MQ
./mbp_testSample.sh

Dec24-19: this is from last spring, so I am guessing, but i think that I prob stopped
dev on this while I figured out local AWS Dynamo. I am not done yet w/ local.
Presumably, I'd then know dynamo and get back to MQ on AWS (serverless, was it?) to write to AWS Dynamo (non local)

Actually, @see evernote ShipShapeAwsApi which currently reads:
April 21, 2019

I believe I installed aws-iot-device-sdk in error.
As I will not right now be using this to connect right away to MQTT.
Instead, I will connect node to Dynamo to get data
. TheMQTT sdk I expect to use someday to replace the python writer to the IoT shadow.
