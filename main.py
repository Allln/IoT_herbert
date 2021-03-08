#!/usr/bin/env python
# coding: utf-8


from umqtt.simple import MQTTClient
from json import dumps
import json
import time
import machine
from machine import RTC
import onewire, ds18x20
import network
import ntptime
import utime
from ntptime import settime

SERVER_MQTT = '147.228.124.68'
#TOPIC = 'ite/blue/sensor'
TOPIC = 'ite/blue/sensor'


rtc = machine.RTC()

# The callback for when a PUBLISH message is received from the server.
def send2broker(client, topic, payload, qos=0, retain=False):
    client.publish(topic, payload, qos=qos, retain=False)


def on_publish(client, userdata, mid):
    print('Published: ', str(mid))
    pass
    

    
def json_c(temp_v,sta_if, buffer):
    if sta_if.isconnected():
        try:
            settime()
        except:
            pass
        time = utime.localtime()
        years = time[0]
        month = time[1]
        day = time[2]
        hour = time[3]
        minute = time[4]
        second = time[5]
        time_res ="{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000Z".format(years,month,day,hour,minute,second)
        
        #encode obj. to json
        temp_final = "{0:.2f}".format(temp_v)
        temp_json = json.dumps({'ite_message': 
                                {'team_name': "blue", 
                                 'created_on': time_res, 
                                 'temperature':temp_final}})
        rtc.datetime([time[0],time[1], time[2], time[6], time[3], time[4],time[5], 0])
        #(year, month, day, weekday, hours, minutes, seconds, subseconds)
        
        #mqtt connect
        try:
            mqttCon = MQTTClient("umqtt_client", SERVER_MQTT, user = "kitt",password = "itejefaktzabava")
            mqttCon.connect()
            if buffer != []:
                for i in buffer:
                    mqttCon.publish(TOPIC, i)
                del buffer[:]
            mqttCon.publish(TOPIC, temp_json)
            mqttCon.disconnect()
        except:
            print("Failed to send json...")
            buffer.append(temp_json)
            
        
    else:
        time = rtc.datetime()
        years = time[0]
        month = time[1]
        day = time[2]
        hour = time[4]
        minute = time[5]
        second = time[6]
        time_res ="{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(years,month,day,hour,minute,second)
        temp_finale = "{0:.2f}".format(temp_v)
        #encode obj. to json
        temp_json = json.dumps({'ite_message': 
                                {'team_name': "blue", 
                                 'created_on': time_res, 
                                 'temperature':temp_finale}})
        buffer.append(temp_json)
        

def main():
    counter = 0
    buffer = []
    #settime()
    led = machine.Pin(0,machine.Pin.OUT)
    
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(b'IoT-CIV', 'UWBc9v.505.i0t')
    #sta_if.connect("brap", "potvorov")
    led.off()
    
    while(not sta_if.isconnected()):
        print("Herbert is trying to connect to wifi...")
        led.off()
        time.sleep_ms(1000)
        led.on()
        time.sleep_ms(1000)
        
    print("Herbert connected successfully.")
    times = utime.localtime()
    rtc.datetime([times[0],times[1], times[2], times[6] , times[3], times[4],times[5],0])
    led.on()
    dat = machine.Pin(12)
    ds = ds18x20.DS18X20(onewire.OneWire(dat))
    temps = ds.scan()
    
    while(True):
        utime.sleep_ms(59500)
        for temp in temps:
            ds.convert_temp()
            temp_value = (ds.read_temp(temp))
            print(temp_value)
            led.off()
            json_c(temp_value, sta_if, buffer)
            led.on()
               
                
if __name__ == '__main__':
    main()