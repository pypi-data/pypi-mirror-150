import smbus
import time
import os
from .board import checkVersion
from .baro import Barometer
from .temperature import TemperatureSensor
from .imu import Accelerometer3, Accelerometer4, Accelerometer5, Magnetometer3, Magnetometer4, Magnetometer5, Gyroscope
from .rgb_ir import RgbIrSensor
from .uva import UvaSensor
from .rtc import RealTimeClock
from .leds import Leds
from .arducam import Camera


boardVersion = checkVersion()

bus = smbus.SMBus(1)

barometer = Barometer(bus, 0x76)
bottom_thermometer = TemperatureSensor(bus, 0x48)
top_thermometer = TemperatureSensor(bus, 0x49)


if boardVersion == "3":
    accelerometer = Accelerometer3(bus, 0x1D)
    magnetometer = Magnetometer3(bus, 0x1D)
    gyroscope = Gyroscope(bus, 0x6B)
    rgb_ir_sensor = RgbIrSensor(bus, 0x52)
    uva_sensor = UvaSensor(bus, 0x38)

elif boardVersion == "4":
    accelerometer = Accelerometer4(bus, 0x6B)
    magnetometer = Magnetometer4(bus, 0x1E)
    gyroscope = Gyroscope(bus, 0x6B)
    uva_sensor = UvaSensor(bus, 0x38)
    rgb_ir_sensor = RgbIrSensor(bus, 0x52)

elif boardVersion == "5":
    accelerometer = Accelerometer5(bus, 0x1D)
    magnetometer = Magnetometer5(bus, 0x1D)
    gyroscope = Gyroscope(bus, 0x6B)
    uva_sensor = UvaSensor(bus, 0x52)
    rgb_ir_sensor = RgbIrSensor(bus, 0x10)

real_time_clock = RealTimeClock(bus, 0x51)

if boardVersion == "3":
    sensors = [
        barometer,
        bottom_thermometer,
        top_thermometer,
        accelerometer,
        gyroscope,
        rgb_ir_sensor,
        uva_sensor,
        real_time_clock
    ]

elif boardVersion == "4":
    sensors = [
        barometer,
        bottom_thermometer,
        top_thermometer,
        accelerometer,
        magnetometer,
        rgb_ir_sensor,
        uva_sensor,
        real_time_clock
    ]
elif boardVersion == "5":
    sensors = [
        barometer,
        bottom_thermometer,
        top_thermometer,
        accelerometer,
        gyroscope,
        magnetometer,
        rgb_ir_sensor,
        uva_sensor,
        real_time_clock
    ]

RgbIrSensor(bus, 0x52).pack_and_write(0x00, 'B', 0b00000110) #UV-A Initialization

for sensor in sensors:
    sensor.configure({})


if boardVersion == "4":
    # gyroscope fails self-test in version 4 but still works
    # skip self-test but still needs to be configured
    gyroscope.configure({})

# Sensor-check muted since already checked
for sensor in sensors:
    assert sensor.self_test(), 'Failed to initialise sensor {}'.format(repr(sensor))

leds = Leds()
camera = Camera()

def test():
    print("RUNNING TEST...")
    try:

        print(barometer.measure().pressure)
        print(barometer.measure().humidity)
        print(barometer.measure().temperature)
        print(bottom_thermometer.measure())
        print(top_thermometer.measure())
        print(accelerometer.measure())
        print(rgb_ir_sensor.measure())
        print(uva_sensor.measure())
        print(real_time_clock.measure())
        leds.set_blue("off")
        leds.set_green("off")
        leds.set_red("off")
        leds.set_led1("off")
        leds.set_led2("off")
        time.sleep(0.25)
        leds.set_led1("on")
        time.sleep(0.25)
        leds.set_led1("off")
        leds.set_led2("on")
        time.sleep(0.25)
        leds.set_led2("off")
        leds.set_red("on")
        time.sleep(0.25)
        leds.set_red("off")
        leds.set_green("on")
        time.sleep(0.25)
        leds.set_green("off")
        leds.set_blue("on")
        time.sleep(0.25)
        leds.set_blue("off")
    except:
        print("ERROR")
        return
    print("PASS")

__all__ = (
    'barometer',
    'bottom_thermometer',
    'top_thermometer',
    'accelerometer',
    'gyroscope',
    'magnetometer',
    'rgb_ir_sensor',
    'uva_sensor',
    'real_time_clock',
    'leds',
    'camera',
    'test'
)







