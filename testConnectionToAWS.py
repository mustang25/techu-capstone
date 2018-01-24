import os
from sense_hat import SenseHat
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from time import sleep, time
from datetime import datetime
import json

sense = SenseHat()


# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return (res.replace("temp=", "").replace("'C\n", ""))


# Custom Shadow callback for AWS IOT
def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")
        print("property: " + str(payloadDict))
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")


def customShadowCallback_Delete(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Delete request with token: " + token + " accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!")


clientId = "a2jhse166el0hk.iot.us-east-1.amazonaws.com"  # REST API Endpoint for thing shadow found in "Manage->Things->Interact"
rootCA = "connect_device_package/root-CA.crt"  # Certificate authority
privateKey = "connect_device_package/weather_lga_6-102.private.key"
publicKey = "connect_device_package/weather_lga_6-102.public.key"
pemCert = "connect_device_package/weather_lga_6-102.cert.pem"

# For certificate based connection
myShadowClient = AWSIoTMQTTShadowClient(clientId)
# Configurations
# For TLS mutual authentication

myShadowClient.configureEndpoint(clientId, 8883)
# For Websocket
# myShadowClient.configureEndpoint("YOUR.ENDPOINT", 443)
myShadowClient.configureCredentials(rootCA, privateKey, pemCert)
# For Websocket, we only need to configure the root CA
# myShadowClient.configureCredentials("YOUR/ROOT/CA/PATH")
myShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

myShadowClient.connect()

myDeviceShadow = myShadowClient.createShadowHandlerWithName("weather_lga_6-102", True)

myDeviceShadow.shadowDelete(customShadowCallback_Delete, 5)

while True:
    # Get current date/time
    time_stamp = time()
    current_date = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d')
    current_time = datetime.fromtimestamp(time_stamp).strftime('%H:%M:%S')

    # Get CPU temperature and convert to float
    cpuTemp = getCPUtemperature()
    cpuTemp = float(cpuTemp)

    # Take readings from all three sensors
    sensorTemp = sense.get_temperature()
    sensor_pressure = round(sense.get_pressure(), 0)
    sensor_humidity = round(sense.get_humidity(), 1)

    # Calibrated Sensor Temp via Github
    temp_calibrated = sensorTemp - ((cpuTemp - sensorTemp) / 5.466)

    # Convert Celsius to Fahreheit
    temp_calibrated = (9 / 5) * temp_calibrated + 32

    # Round the values to one decimal place
    temp_calibrated = round(temp_calibrated, 1)

    # Create the message
    # str() converts the value to a string so it can be concatenated
    JSONPayload = {
        "state": {
            "reported": {
                "date": current_date,
                "time": current_time,
                "temperature": temp_calibrated,
                "humidity": sensor_humidity,
                "pressure": sensor_pressure
            }
        }
    }

    myDeviceShadow.shadowUpdate(json.dumps(JSONPayload), customShadowCallback_Update, 5)
    sleep(10)
