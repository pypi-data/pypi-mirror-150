
from .i2c import I2cDevice
from .telemetry import Telemetry
from collections import namedtuple
from .board import checkVersion
import smbus
import time

boardVersion = checkVersion()

if boardVersion == "4" or boardVersion == "3":

    UvaMeasurement = namedtuple(
        'UvaMeasurement',
        'uva'
    )


    class UvaSensor(I2cDevice):
        def self_test(self):
            # There is nothing to do here, only readable registers are the output data
            return True

        def configure(self, args):
            self.bus.write_byte(0x38, 0x60)

        def measure(self):
            """
            :return: UVa reading in W m^-2
            """
            # scale from sensor is 5 uW / cm^2  / encoder count.
            msb = self.bus.read_byte(0x39)
            lsb = self.bus.read_byte(0x38)
            result = UvaMeasurement(((msb << 8) | lsb) * 5e-2)
            packet = {
                "uva": str(result.uva)
            }
            Telemetry.update("uva", packet)
            return result

        @property
        def uva(self):
            return self.measure().uva

else:

    UvaMeasurement = namedtuple(
        'UvaMeasurement',
        'uva'
    )

    class UvaSensor(I2cDevice):

        def self_test(self):
            # There is nothing to do here, only readable registers are the output data
            return True

        #def configure(self, args):
            #self.bus.write_byte(0x52, 0x60)

        def measure(self):
            """
            :return: UVa reading in W m^-2
            """
            # APDS9200
            # Get I2C bus
            bus = smbus.SMBus(1)

            # APDS9200 address, 0x52
            # Send power on command
            #		0x00	Power On
            #       0x02    Set sensor

            bus.write_byte(0x52, 0x00)
            time.sleep(0.2)
            bus.write_byte(0x52, 0x01)
            time.sleep(0.2)
            bus.write_byte(0x52, 0x05)
            time.sleep(0.2)
            bus.write_byte(0x52, 0x07)
            time.sleep(0.2)

            #self.write(0x00, [0b00011010])
            #self.write(0x01, [0b00100010])
            #self.write(0x05, [0b00000001])
            #self.write(0x07, [0b00100000])


            # APDS9200 address, 0x52
            # Read data. LSB-UV, UV, MSB-UV

            bus.write_byte(0x52, 0x10)
            time.sleep(0.2)
            msb = bus.read_byte_data(0x52, 0x10)

            bus.write_byte(0x52, 0x11)
            time.sleep(0.2)
            nsb = bus.read_byte_data(0x52, 0x11)

            bus.write_byte(0x52, 0x12)
            time.sleep(0.2)
            lsb = bus.read_byte_data(0x52, 0x12)

            #bus.write_byte(0x52, 0x10)
            #time.sleep(0.3)
            #msb = self.bus.read_byte(0x52)
            #time.sleep(0.3)

            #bus.write_byte(0x52, 0x11)
            #time.sleep(0.3)
            #nsb = self.bus.read_byte(0x52)
            #time.sleep(0.3)

            #bus.write_byte(0x52, 0x12)
            #time.sleep(0.3)
            #lsb = self.bus.read_byte(0x52)
            #time.sleep(0.3)

            UV_TOT = msb + nsb * 256 + lsb * 4096 #msb 0:7, nsb 0:7, lsb 0:3 -> 12 bit, 2^12=4096


            result = UvaMeasurement(UV_TOT / 40) #UV Index 1 = 0.025 W/m²

            packet = {
                "uva": str(result.uva)
            }
            Telemetry.update("uva", packet)
            return result


        @property
        def uva(self):
            return self.measure().uva



