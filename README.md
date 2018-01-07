# pycom
First esp8266 code that doesn't crash the processor.

## To run.  Install the pycom interpreter on the ESP8266
 * Follow steps here:
  https://learn.adafruit.com/micropython-basics-how-to-load-micropython-on-a-board/esp8266
 * The follow steps to install ampy:
  https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy

## Assuming ampy is installed upload code:
export AMPY_PORT=/dev/tty.SLAB_USBtoUART
 * Try it:
   ampy run main.py
 * Upload it:
   ampy put main.py
