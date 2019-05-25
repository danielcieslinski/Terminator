import RPi.GPIO as GPIO
from time import sleep, time
import threading

class Controller:
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


class Vehicle:
    def __init__(self, right_pins, left_pins):
        self.right_wheels = Controller(right_pins[0], right_pins[1])
        self.left_wheels = Controller(left_pins[0], left_pins[1])

    def forward(self, duration):
        return self.__run(duration, [self.left_wheels.forward, self.right_wheels.backward])

    def backward(self, duration):
        return self.__run(duration, [self.left_wheels.backward, self.right_wheels.backward])

    def turn_left(self, duration):
        return self.__run(duration, [self.left_wheels.backward, self.right_wheels.forward])

    def turn_right(self, duration):
        return self.__run(duration, [self.left_wheels.forward, self.right_wheels.backward])

    def __run(self, duration, args):
        ths = [threading.Thread(target=line, args=(duration,)) for line in args]
        for th in ths: th.start()
        for th in ths: th.join()


class Sensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def check(self):
        return (GPIO.input(self.pin) == 0)

    def loop(self):
        """
        Only for debug. Use check in deamon
        """
        while True:
            if (self.check()):
                print("Detected")
            else:
                print("----")


class HCSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def distance(self):
        GPIO.output(self.trigger_pin, True)
        sleep(0.0001)
        GPIO.output(self.trigger_pin, False)

        start_time = time()
        stop_time = time()

        while GPIO.input(self.echo_pin) == 0:
            start_time = time()

        while GPIO.input(self.echo_pin) == 1:
            stop_time = time()

        time_elapsed = stop_time - start_time
        distance = (time_elapsed * 34300) / 2

        return distance

    def loop(self, interval):
        """
        Only for debug, use distance in daemon
        """
        try:
            while True:
                dist = self.distance()
                print("Measured Distance = %.1f cm" % dist)
                sleep(interval)

        except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()

