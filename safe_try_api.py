import RPi.GPIO as GPIO
from time import sleep
import threading

class Wheel:
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

class WheelsLine:
    def __init__(self, front_pins, rear_pins):
        self.front_wheel = Wheel(front_pins[0], front_pins[1])
        self.rear_wheel = Wheel(rear_pins[0], rear_pins[1])

    def forward(self, duration):
        th1 = threading.Thread(target=self.front_wheel.forward, args=(duration,))
        th2 = threading.Thread(target=self.rear_wheel.forward, args=(duration,))
        th1.start()
        th2.start()
        sleep(duration)

    def backward(self, duration):
        th1 = threading.Thread(target=self.front_wheel.backward, args=(duration,))
        th2 = threading.Thread(target=self.rear_wheel.backward, args=(duration,))
        th1.start()
        th2.start()
        sleep(duration)

    def __del__(self):
        del self.front_wheel, self.rear_wheel

class Vehicle:
    def __init__(self, right_pins, left_pins):
        """
        :param right_pins: [ [front_forward_pin, front_backward_pin], [rear_forward_pin, rear_backward_pin]
        :param left_pins:
        """

if __name__ == '__main__':

    right = WheelsLine([40, 38], [16,18])
    right.forward(2)
    GPIO.cleanup()
