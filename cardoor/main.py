from machine import Pin
import machine
import utime
import ustruct
import time
import usocket

import gc
from urequests import get

print('Hello world! I can count to 10:')
for i in range(1,11):
    print(i)

import ubinascii
import network
print ('Mac: ', ubinascii.hexlify(machine.unique_id(),':').decode())

# create an output pin on pin #0
print('Setup the pin...')

pinOutput = Pin(16, Pin.OUT)
pinOutput.value(1);

pinInput = Pin(17, Pin.IN, Pin.PULL_DOWN)
def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    nets = wlan.scan()
    count = 0
    for net in nets:
        print("Ssid:");
        print(str(net[0]), str(net[4]));
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect("IBF", "*********")
        while not wlan.isconnected():
            count = count + 1
            if count > 10:
                break;
            pass
    print('network config:', wlan.ifconfig())

def retrieve_url(url):
    #gc.collect()
    resp = None
    try:
        print ("Getting url", url);
        resp = get(url)
        print (resp);
        value = resp.text
    except Exception as e: # Here it catches any error.
        if isinstance(e, OSError) and resp: # If the error is an OSError the socket has to be closed.
            resp.close()
        value = {"error": e}
    #gc.collect()
    return value

do_connect()
print('Network is setup.')

#addr = usocket.getaddrinfo("192.168.2.204", 5005)[0][-1];
#addr = usocket.getaddrinfo("192.168.2.38", 3001)[0][-1];

switch_data = pinInput.value();
while True:
    cur_value = pinInput.value();
    print ("Switch:", switch_data, cur_value);
    if cur_value != switch_data:
        switch_data = cur_value
        res = retrieve_url('https://ardvarkfun.com/iotbutton?value=' + str(switch_data));
        print ("Url result:", str(cur_value), res);
    time.sleep(.3)
