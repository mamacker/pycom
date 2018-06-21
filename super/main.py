import machine, neopixel
import utime
import gc
import ubinascii
from urequests import get

np_pin = machine.Pin(12, machine.Pin.OUT)
pinInput = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)

np = neopixel.NeoPixel(np_pin, 32, timing=True)

val = "family0"
val_color = (255,0,0)
#val = "family1"
#val_color = (125,125,125)
#val = "family2"
#val_color = (0,0,255)

for i in range(np.n):
    np[i] = val_color
np.write()

print ('Mac: ', ubinascii.hexlify(machine.unique_id(),':').decode())

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('TRI Robots', 'FIKCUPhUe#f3L6J7')
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

def clear_lights():
    for i in range(np.n):
        np[i] = val_color;
    np.write()

do_connect()
print('Network is setup.')

last_blink = utime.ticks_ms()
last_server_check = utime.ticks_ms()
blink_on = True
caller_pinged = False

last_server_val = 0;
while True:
    if utime.ticks_ms() - last_server_check > 5000:
        # Check the button state on the server.
        print ("Calling the server for get");
        res = retrieve_url('http://10.110.120.85:3000/button/get?which=' + str(val))

        print ("Result: " + str(res));
        try: 
            if int(res + "") > last_server_val:
                print ("Button set... starting blink.");
                if not caller_pinged:
                    caller_pinged = True
                    blink_on = True
                    last_blink = utime.ticks_ms()
            else:
                print ("Button not set clearing blink.");
                caller_pinged = False
                clear_lights()
            last_server_check = utime.ticks_ms()
        except:
            print ("Exception in result:" + str(res));

    # Handle the blinking if it was set.
    if caller_pinged and utime.ticks_ms() - last_blink > 300:
        print ("Blinking: " + str(last_blink))
        if blink_on:
            for i in range(np.n):
                np[i] = val_color
            np.write()
        else:
            clear_lights()
        last_blink = utime.ticks_ms()
        blink_on = not blink_on

    # Watch the pin to see if we need to set our
    # state on the server
    if pinInput.value() == 0:
        if caller_pinged:
            print("Setting button CLEARED with server...");
            retrieve_url('http://10.110.120.85:3000/button/clear?which=' + str(val))
            caller_pinged = False
            clear_lights();
        else:
            print("Setting button on with server...");
            blink_on = True
            last_blink = utime.ticks_ms()
            retrieve_url('http://10.110.120.85:3000/button/set?which=' + str(val))
            caller_pinged = True

