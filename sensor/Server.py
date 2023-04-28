#Setup Dweet
#Dweet Loop

from sense_hat import SenseHat
import time
from datetime import datetime
import paho.mqtt.publish as publish
import psutil
from sds011 import *
import aqi



#Setup sensehat and SDS011
sensor = SDS011("/dev/ttyUSB0")
sense = SenseHat()

def main():
    getSenseHat()
    getSDS011()


#get sensehat environment info
def getSenseHat():
    t = sense.get_temperature()
    p = sense.get_pressure()
    h = sense.get_humidity()
    
    t = round(t,1)
    p = round(p,1)
    h = round(h,1)
        
    msg = "Temp = %s C, Pressure = %s mbar, Humidity =%s" % (t, p, h)
        
    sense.show_message(msg, scroll_speed=0.05)
    return


def get_data(n=3):
        sensor.sleep(sleep=False)
        pmt_2_5 = 0
        pmt_10 = 0
        time.sleep(10)
        for i in range (n):
            x = sensor.query()
            pmt_2_5 = pmt_2_5 + x[0]
            pmt_10 = pmt_10 + x[1]
            time.sleep(2)
        pmt_2_5 = round(pmt_2_5/n, 1)
        pmt_10 = round(pmt_10/n, 1)
        sensor.sleep(sleep=True)
        time.sleep(2)
        return pmt_2_5, pmt_10
    

def conv_aqi(pmt_2_5, pmt_10):
    aqi_2_5 = aqi.to_iaqi(aqi.POLLUTANT_PM25, str(pmt_2_5))
    aqi_10 = aqi.to_iaqi(aqi.POLLUTANT_PM10, str(pmt_10))
    return aqi_2_5, aqi_10


def save_log(pmt_2_5, aqi_2_5, pmt_10, aqi_10):        
    with open("/home/pi/Desktop/Spring2023/AQVS/air_quality.csv", "a") as log:
        dt = datetime.now()
        log.write("{},{},{},{},{}\n".format(dt, pmt_2_5, aqi_2_5, pmt_10, aqi_10))
    log.close()

def get_data(n=3):
        sensor.sleep(sleep=False)
        pmt_2_5 = 0
        pmt_10 = 0
        time.sleep(10)
        for i in range (n):
            x = sensor.query()
            pmt_2_5 = pmt_2_5 + x[0]
            pmt_10 = pmt_10 + x[1]
            time.sleep(2)
        pmt_2_5 = round(pmt_2_5/n, 1)
        pmt_10 = round(pmt_10/n, 1)
        sensor.sleep(sleep=True)
        time.sleep(2)
        return pmt_2_5, pmt_10
    
#get SDS011 info
def getSDS011():
    pmt_2_5, pmt_10 = get_data()
    aqi_2_5, aqi_10 = conv_aqi(pmt_2_5, pmt_10)
    tPayload = "field1=" + str(pmt_2_5)+ "&field2=" + str(aqi_2_5)+ "&field3=" + str(pmt_10)+ "&field4=" + str(aqi_10)
    try:
        save_log(pmt_2_5, aqi_2_5, pmt_10, aqi_10)
        time.sleep(15)
    except Exception as e:
        print(e)
        time.sleep(12)
        
    return

if __name__ == "__main__":
    main()
   