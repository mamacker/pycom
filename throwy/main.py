from machine import Pin
import utime
import ustruct
import time
import usocket

import gc
from urequests import get
from machine import I2C
i2c = I2C(sda=Pin(23), scl=Pin(22), freq=400000)

from vl53l0x import VL53L0X

print('Hello world! I can count to 10:')
for i in range(1,11):
    print(i)

# create an output pin on pin #0
print('Setup the pin...')
pin = Pin(12, Pin.OUT)

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('ACME', 'roadrunner')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def select_channel(channel):
    i2c.writeto(0x74, ustruct.pack('>B', 1 << channel ))
    print ("Selected: ", channel, ustruct.pack('>B', 1 << channel ))

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

for i in range(4,7):
    select_channel(i);
    dist = VL53L0X(i2c);
    dist.measurement_timing_budget = 20000;
    #dist.io_timeout_s = 3000;

    print("Identifying.");
    print("Range: ", dist.range)
#addr = usocket.getaddrinfo("192.168.2.204", 5005)[0][-1];
addr = usocket.getaddrinfo("192.168.2.38", 3001)[0][-1];

times = 0
while True:
    select_channel(times % 3 + 4);
    dist.start_range();
    r = dist.range
    print ("Range");
    print (r);
    times = times + 1

    #s = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
    #s.sendto(ustruct.pack('>H',r), addr);
    #s.close()
    #res = retrieve_url('http://192.168.2.38:3000/add?source=throwy1&stat=vl6180&type=sample&value=' + str(dist.range() - 15));
