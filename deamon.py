import RPi.GPIO as GPIO
from terminator_api import *
from constants import *

CANDLE_DISTANCE = 15


class Daemon:
    def __init__(self):
        self.vehicle = Vehicle((RIGHT_FORWARD, RIGHT_BACKWARD), (LEFT_FORWARD, LEFT_BACKWARD))
        self.fan = Controller(FAN_FORWARD, FAN_BACKWARD)
        self.hc_sensor = HCSensor(TRIGGER_PIN, ECHO_PIN)
        self.flame_sensor = Sensor(FLAME_PIN)

    def loop(self):
        while True:
            self.find_flame()
            if self.drive_while_can(): self.extinguish()
            else: pass

    def find_flame(self):
        while True:
            self.vehicle.turn_right(0.01)
            if self.flame_sensor.check():
                return

    def drive_while_can(self):
        while self.hc_sensor.distance() > CANDLE_DISTANCE and self.flame_sensor.check():
            self.vehicle.forward(0.02)

        return self.flame_sensor.check()

    def extinguish(self):
        print("extuinsds")
        self.fan.forward(5)
        self.vehicle.backward(1)


if __name__ == '__main__':
    daemon = Daemon()
    try:
        daemon.loop()
    except:
        GPIO.cleanup()
