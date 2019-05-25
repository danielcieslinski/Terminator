import RPi.GPIO as GPIO
from terminator_api import *
from constants import *

CANDLE_DISTANCE = 10
NULL_DISTANCE = 30

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
                print("found")
                return

    def drive_while_can(self):
        sleep(1)
        self.vehicle.forward(0.1)
        self.vehicle.turn_right(0.3)
        while self.hc_sensor.distance() > CANDLE_DISTANCE and self.flame_sensor.check():
            while self.hc_sensor.distance() > NULL_DISTANCE:
                    self.vehicle.turn_right(0.05)

            print("quiting")

            self.vehicle.forward(0.05)
            print("Driving forward")

        return self.flame_sensor.check()

    def extinguish(self):
        print("extuinsds")
        self.fan.forward(10)
        self.vehicle.backward(0.7)
        self.vehicle.turn_left(0.3)
        sleep(1)


if __name__ == '__main__':
    daemon = Daemon()
    try:
        daemon.loop()
    except Exception as e:
        print(e)
        GPIO.cleanup()
