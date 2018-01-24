import os
from sense_hat import SenseHat

# Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

sense = SenseHat()

# CPU informatiom
cpuTemp = getCPUtemperature()
sensorTemp = sense.get_temperature()


while True:

    # Get CPU temperature & convert to Float
    cpuTemp = getCPUtemperature()
    cpuTemp = float(cpuTemp)
    

    # Get sensor temperature 
    sensorTemp = sense.get_temperature()

    # Equation to calculate room temp
    roomTemp = cpuTemp - sensorTemp

    # Round the Room Temperature to one decimal place
    #roomTemp = round(roomTemp, 1)

    # Print roomTemp to console
    print(str(roomTemp))

    # Create the message on the LEDs and rotate 180 degrees
    sense.set_rotation(180)
    sense.show_message(str(roomTemp), scroll_speed=0.1)
