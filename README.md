# pycom
First esp8266 code that doesn't crash the processor.

## To run.  Install the pycom interpreter on the ESP8266
 * Follow steps here:
  https://learn.adafruit.com/micropython-basics-how-to-load-micropython-on-a-board/esp8266
 * Which will look like this in the end:
 ** ESP8266
 sudo esptool.py --port /dev/tty.SLAB_USBtoUART  write_flash --flash_size=detect 0 /Users/matt.amacker/Downloads/esp8266-20171101-v1.9.3.bin
 ** ESP32: https://micropython.org/download#esp32
 sudo esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART  write_flash -z 0x1000 ./esp32-20180621-v1.9.4-189-g34344a41.bin
 * The follow steps to install ampy:
  https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy

## Assuming ampy is installed upload code:
export AMPY_PORT=/dev/tty.SLAB_USBtoUART
 * Try it:
   ampy run main.py
 * Upload it:
   ampy put main.py

### To get on:
screen $AMPY_PORT 115200
