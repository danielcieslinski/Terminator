import RPi.GPIO as GPIO
from terminator_api import *
from constants import *

CANDLE_DISTANCE = 15
NULL_DISTANCE = 30

class Daemon:
    def __init__(self):
        self.vehicle = Vehicle((RIGHT_FORWARD, RIGHT_BACKWARD), (LEFT_FORWARD, LEFT_BACKWARD))
        self.fan = Controller(FAN_FORWARD, FAN_BACKWARD)
        self.hc_sensor = HCSensor(TRIGGER_PIN, ECHO_PIN)
        self.flame_sensor = Sensor(FLAME_PIN)
        self.turn = 0 #0 is last was left 1 is last was right

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
        self.vehicle.turn_right(0.2)
        while self.hc_sensor.distance() > CANDLE_DISTANCE and self.flame_sensor.check():
            while self.hc_sensor.distance() > NULL_DISTANCE:
                print("more")
                if not self.turn:
                    self.vehicle.turn_right(0.05)
                else: self.vehicle.turn_left(0.05)

            print("quiting")

            self.turn = not self.turn
            self.vehicle.forward(0.05)
            print("Driving forward")

        return self.flame_sensor.check()

    def extinguish(self):
        print("extuinsds")
        self.fan.forward(8)
        self.vehicle.backward(0.4)
        self.vehicle.turn_left(0.3)
        self.turn = not self.turn


if __name__ == '__main__':
    daemon = Daemon()
    try:
        daemon.loop()
    except Exception as e:
        print(e)
        GPIO.cleanup()
