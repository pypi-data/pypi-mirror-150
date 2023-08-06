
from .i2c import I2cDevice
from .telemetry import Telemetry
from collections import namedtuple
from .board import checkVersion
import smbus
import time

boardVersion = checkVersion()

if boardVersion == "4" or boardVersion == "3":

    RgbIrMeasurement = namedtuple(
        'RgbIrMeasurement',
        'red green blue ir'
    )


    def _parse_rgb_ir_bytes(colour_data):
        measurement = tuple((colour_data[2 * i + 1] << 16) | colour_data[2 * i] for i in range(4))
        total = sum(measurement)
        if total == 0:
            return 0, 0, 0, 0
        measurement = tuple(x / total for x in measurement)

        packet = {
            "r": str(measurement[3]),
            "g": str(measurement[1]),
            "b": str(measurement[2]),
            "ir": str(measurement[0])
        }

        Telemetry.update("rgb", packet)
        return measurement[3], measurement[1], measurement[2], measurement[0]


    class RgbIrSensor(I2cDevice):
        def self_test(self):
            id = self.read(0x06, 1)[0]
            return id == 0xB2

        def configure(self, args):
            # set light sensor enabled, colour sensing mode.
            self.pack_and_write(0x00, 'B', 0b00000110)
            super().configure(args)

        def measure(self):
            """
            :return: R, G, B and IR Channel readings and a fraction of the total.
            """
            colour_data = self.read_and_unpack(0x0A, '<BHBHBHBH')
            return RgbIrMeasurement(*_parse_rgb_ir_bytes(colour_data))

        @property
        def red(self):
            return self.measure()[0]

        @property
        def green(self):
            return self.measure()[1]

        @property
        def blue(self):
            return self.measure()[2]

        @property
        def ir(self):
            return self.measure()[3]

else:

    RgbIrMeasurement = namedtuple(
        'RgbIrMeasurement',
        'red green blue ir'
    )

    def _parse_rgb_ir_bytes(colour_data):
        measurement = tuple((colour_data[2 * i + 1] << 16) | colour_data[2 * i] for i in range(4))
        total = sum(measurement)
        if total == 0:
            return 0, 0, 0, 0
        measurement = tuple(x / total for x in measurement)

        packet = {
            "r": str(measurement[3]),
            "g": str(measurement[1]),
            "b": str(measurement[2]),
            "ir": str(measurement[0])
        }

        Telemetry.update("rgb", packet)
        return measurement[3], measurement[1], measurement[2], measurement[0]

    class RgbIrSensor(I2cDevice):

        def self_test(self):
            id = self.read(0x0C, 1)[0]
            return id == 0x28


        def measure(self):
            """
            :return: R, G, B and IR Channel readings and a fraction of the total.
            """

            # VEML3328
            # Get I2C bus
            bus = smbus.SMBus(1)

            # VEML3328 address, 0x10
            # Send power on command and set deault data gain (x1)

            bus.write_i2c_block_data(0x10, 0x00, [0x00, 0x00])

            time.sleep(0.5)

            # VEML3328 address, 0x10
            # Read data back, 2 bytes each register
            # RGB-IR MSB, RGB-IR LSB


            Rdata = bus.read_i2c_block_data(0x10, 0x05, 2)
            Gdata = bus.read_i2c_block_data(0x10, 0x06, 2)
            Bdata = bus.read_i2c_block_data(0x10, 0x07, 2)
            IRdata = bus.read_i2c_block_data(0x10, 0x08, 2)

            # Convert the data from mlux to lux
            # Clear = (Cdata[0] * 256 + Cdata[1])  / 1000

            #Red = (Rdata[0] + Rdata[1] * 256) / 1000
            #Green = (Gdata[0] + Gdata[1] * 256) / 1000
            #Blue = (Bdata[0] + Bdata[1] * 256) / 1000
            #IR = (IRdata[0] * 256 + IRdata[1]) / 1000

            # Convert the data from lux to W/m²

            #RedWm2 = Red * 0.0079
            #GreenWm2 = Green * 0.0079
            #BlueWm2 = Blue * 0.0079
            #IRWm2 = IR * 0.0079

            colour_data = bytearray()  # New empty byte array# Append data to the array

            colour_data.extend(IRdata[1].to_bytes(1, byteorder='big'))
            colour_data.extend(IRdata[0].to_bytes(1, byteorder='big'))
            colour_data.extend(Gdata[1].to_bytes(1, byteorder='big'))
            colour_data.extend(Gdata[0].to_bytes(1, byteorder='big'))
            colour_data.extend(Bdata[1].to_bytes(1, byteorder='big'))
            colour_data.extend(Bdata[0].to_bytes(1, byteorder='big'))
            colour_data.extend(Rdata[1].to_bytes(1, byteorder='big'))
            colour_data.extend(Rdata[0].to_bytes(1, byteorder='big'))

            #print("Red0 : ", Rdata[0])
            #print("Red1 : ", Rdata[1]*256)
            #print("Green0 : ", Gdata[0])
            #print("Green1 : ", Gdata[1]*256)
            #print("Blue0 : ", Bdata[0])
            #print("Blue1 : ", Bdata[1]*256)
            #print("IR0 : ", IRdata[0])
            #print("IR1 : ", IRdata[1]*256)

            return RgbIrMeasurement(*_parse_rgb_ir_bytes(colour_data))


        @property
        def red(self):
            return RedWm2

        @property
        def green(self):
            return GreenWm2

        @property
        def blue(self):
            return BlueWm2

        @property
        def ir(self):
            return IRWm2



        # Output data to screen








