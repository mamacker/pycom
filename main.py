from machine import Pin
import utime
import ustruct
import time
import usocket

import gc
from urequests import get
from machine import I2C
i2c = I2C(sda=Pin(23), scl=Pin(22), freq=400000)

from vl6180 import Sensor

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
    i2c.writeto(0x70, ustruct.pack('>HB', 0x04, channel))

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

select_channel(5);
dist = Sensor(i2c, 0x60);

for i in range(5,7):
    select_channel(i);
    dist.init();

print("Identifying.");
print(dist.identify())
#addr = usocket.getaddrinfo("192.168.2.204", 5005)[0][-1];
addr = usocket.getaddrinfo("192.168.2.38", 3001)[0][-1];

times = 0
while True:
    if times % 50 == 0:
        dist.init()
        if times > 10000000:
            times = 0
    select_channel((times % 4 == 0) + 4);
    r = dist.range()
    print ("Range");
    print (r);
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
    s.sendto(ustruct.pack('>H',r), addr);
    s.close()
    #res = retrieve_url('http://192.168.2.38:3000/add?source=throwy1&stat=vl6180&type=sample&value=' + str(dist.range() - 15));
