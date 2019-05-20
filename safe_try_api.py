import RPi.GPIO as GPIO
from time import sleep
from constants import *


class Wheel:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        """
        Pins to be adjusted to corresponding wheels
        """
        GPIO.setup(FORWARD_PIN, GPIO.OUT)
        GPIO.setup(BACKWARD_PIN, GPIO.OUT)

    def foreward(self, duration):
        GPIO.output(BACKWARD_PIN, GPIO.LOW)
        GPIO.output(FORWARD_PIN, GPIO.HIGH)
        sleep(duration)
        GPIO.output(FORWARD_PIN, GPIO.LOW)

    #
    # def backward(self, power, duration):
    #     GPIO.output(BACKWARD_PIN, )
    #     GPIO.output(FORWARD_PIN, False)
    #     self.run(power, duration)


if __name__ == '__main__':
    wheel = Wheel()
    wheel.foreward(2)
    GPIO.cleanup()