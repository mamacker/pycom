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

pinInput = Pin(17, Pin.IN)

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('TRI Guest WiFi', 'tri welcomes you')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def retrieve_url(url):
    #gc.collect()
    resp = None
    try:
        resp = get(url)
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
    '''
    if cur_value != switch_data:
        switch_data = cur_value
        res = retrieve_url('http://192.168.10.50:3000/switch?source=door1&value=' + str(switch_data));
    '''
    time.sleep(.3)
