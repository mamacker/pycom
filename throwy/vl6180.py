import ustruct
import time

# VCNL4040 constants:
VCNL4040_ALS_CONF            = 0x00
VCNL4040_PS_CONF1            = 0x03 # NOTE: this also covers PSCONF2 reg
VCNL4040_PS_CONF3            = 0x04 # NOTE: this also covers PSMS reg
VCNL4040_PS_DATA             = 0x08
VCNL4040_PS_DATAL             = 0x0008
VCNL4040_ALS_DATA            = 0x09
VCNL4040_INT_FLAG            = 0x0B # NOTE: this is the high byte
VCNL4040_DEVICE_REG          = 0x0C
VCNL4040_DEVICE_ID           = 0x186 # Value expected in the DEVICE_REG


class Sensor:
    def __init__(self, i2c, address=0x29):
        self.i2c = i2c
        self._address = address
        self.init()

    def _set_reg8(self, address, value):
        data = ustruct.pack('>HB', address, value)
        try:
            self.i2c.writeto(self._address, data)
        except:
            print("error set reg8");
            None;

    def _set_reg16(self, address, value):
        data = ustruct.pack('>HH', address, value)
        try:
            self.i2c.writeto(self._address, data)
        except:
            print("error set reg16");

    def _get_reg8(self, address):
        self.i2c.start()
        self.i2c.write(ustruct.pack('>BH', self._address << 1, address))
        time.sleep(.001);
        data = [];
        try:
            data = self.i2c.readfrom(self._address, 1)
            return data[0]
        except:
            print("error get reg8");
        return 0

    def _get_reg16(self, address):
        self.i2c.start()
        self.i2c.write(ustruct.pack('>BH', self._address << 1, address))
        time.sleep(.001);
        data = [];
        try:
            data = self.i2c.readfrom(self._address, 2)
            return ustruct.unpack('>B', data)[0]
        except:
            print("error get_reg16");
        return 0

    def init(self):
        # Now that we know we are looking at our device, setup the config.
        self._set_reg16(VCNL4040_ALS_CONF, 0x8000) # ALS enabled, no interrupts
        self._set_reg16(VCNL4040_PS_CONF1, 0b0000111000000000) # high accuracy, and clear the shut down
        self._set_reg16(VCNL4040_PS_CONF3, 0x0005) # no 'smart' modes


    def identify(self):
        print("Identify: ", self._get_reg16(VCNL4040_DEVICE_REG));
        """Retrieve identification information of the sensor."""
        return {
            'model': self._get_reg8(0x0000),
            'revision': (self._get_reg8(0x0001), self._get_reg8(0x0002)),
            'module_revision': (self._get_reg8(0x0003),
                                self._get_reg8(0x0004)),
            'date': self._get_reg16(0x006),
            'time': self._get_reg16(0x008),
        }

    def dump_register_range(self, start, end):
        print ("Printing registers 0x%x -> 0x%x" % (start,end))
        for reg in range(start,end+1):
            val = self._get_reg16(reg)
            print ("[0x%x] 0x%x" % (reg, val))

    def range(self):
        """Measure the distance in millimeters. Takes 0.01s."""
        return self._get_reg16(VCNL4040_PS_DATAL) # Result range value
