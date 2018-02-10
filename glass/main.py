from machine import Pin
import utime
import gc
from urequests import get

from machine import I2C
i2c = I2C(sda=Pin(23), scl=Pin(22), freq=400000)

from machine import ADC
adc = ADC(Pin(32))            # create ADC object on ADC pin
adc.read()              # read value, 0-1024


print('Hello world! I can count to 10:')
for i in range(1,11):
    print(i)

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

pulse = Pin(27, Pin.OUT)
pulse.value(0);
while True:
    pulse.value(1);
    val = adc.read();
    pulse.value(0);

    res = retrieve_url('http://192.168.2.38:3000/' + str(val))
