import RPi.GPIO as GPIO
from time import sleep, time
import threading
from constants import *


class WheelsLine:
    def __init__(self, forward_pin, backward_pin):
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.forward_pin, GPIO.OUT)
        GPIO.setup(self.backward_pin, GPIO.OUT)

    def forward(self, duration):
        GPIO.output(self.forward_pin, GPIO.HIGH)
        sleep(duration)
        GPIO.output(self.forward_pin, GPIO.LOW)

    def backward(self, duration):
        GPIO.output(self.backward_pin, GPIO.HIGH)
        sleep(duration)
        GPIO.output(self.backward_pin, GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()

class Vehicle:
    def __init__(self, right_pins, left_pins):
        self.right_wheels = WheelsLine(right_pins[0], right_pins[1])
        self.left_wheels = WheelsLine(left_pins[0], left_pins[1])

    def forward(self, duration):
        ths = [threading.Thread(target=line.forward, args=(duration,)) for line in [self.left_wheels, self.right_wheels] ]
        for th in ths: th.start()
        for th in ths: th.join()

    def backward(self, duration):
        ths = [threading.Thread(target=line.backward, args=(duration,)) for line in [self.left_wheels, self.right_wheels] ]
        for th in ths: th.start()
        for th in ths: th.join()

    def turn_left(self, duration):
        ths = [threading.Thread(target=line, args=(duration,)) for line in [ self.left_wheels.backward, self.right_wheels.forward ] ]
        for th in ths: th.start()
        for th in ths: th.join()

    def turn_right(self, duration):
        ths = [threading.Thread(target=line, args=(duration,)) for line in [ self.left_wheels.forward, self.right_wheels.backward ] ]
        for th in ths: th.start()
        for th in ths: th.join()

    def __del__(self):
        del self.right_wheels, self.left_wheels

class Sensor:
    def __init__(self, pin, sensor_type):
        self.pin = pin
        self.sensor_type = sensor_type
        GPIO.setmode(GPIO.BOARD)  # Set GPIO by numbers
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def check(self):
        return (GPIO.input(self.pin) == 0)

    def loop(self):
        while True:
            if (self.check()):
                print("{}: Detected".format(self.sensor_type))
            else: print("{}: ----".format(self.sensor_type))

    def __del__(self):
        GPIO.cleanup()

class HCSensor:
    def __init__(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(ECHO_PIN, GPIO.IN)

    def distance(self):
        GPIO.output(TRIGGER_PIN, True)
        # set Trigger after 0.01ms to LOW
        sleep(0.00001)
        GPIO.output(TRIGGER_PIN, False)

        StartTime = time()
        StopTime = time()

        while GPIO.input(ECHO_PIN) == 0:
            StartTime = time()

        while GPIO.input(ECHO_PIN) == 1:
            StopTime = time()

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2

        return distance

    def loop(self, interval):
        try:
            while True:
                dist = self.distance()
                print("Measured Distance = %.1f cm" % dist)
                sleep(interval)

            # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()

if __name__ == '__main__':

    # Sensor(32, )
    sens = HCSensor()
    sens.loop(0.5)

    # sensor = Sensor()
    #
    # try: oas.loop()
    # except: GPIO.cleanup()

    # vehicle = Vehicle([16,18], [40,38])
    # vehicle.forward(5)

    GPIO.cleanup()
