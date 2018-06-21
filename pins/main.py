# Print a nice list of pins, their current settings, and available afs.
# Requires pins_af.py from ports/stm32/build-machineV10/ directory.

import machine

def pins():
    for x in range(1,60):
        print(machine.pin_print(x))
pins()
