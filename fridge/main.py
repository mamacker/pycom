from machine import Pin
import utime
import gc
from urequests import get

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('wobegong', 'monkeybutt')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def retrieve_url(url):
    gc.collect()
    resp = None
    try:
        resp = get(url)
        value = resp.text
    except Exception as e: # Here it catches any error.
        if isinstance(e, OSError) and resp: # If the error is an OSError the socket has to be closed.
            resp.close()
        value = {"error": e}
    gc.collect()
    return value

do_connect()
print('Network is setup.')

while True:
    utime.sleep(60);
    res = retrieve_url('https://theamackers.com/fridge');
    print('Request complete.')
    print(res)

    utime.sleep(3);


