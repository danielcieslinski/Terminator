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
        GPIO.setup(ENABLE_PIN, GPIO.OUT)

        self.pwm = GPIO.PWM(ENABLE_PIN, 100)
        self.pwm.start(0)

    def run(self, power, duration):
        self.pwm.ChangeDutyCycle(power)
        GPIO.output(ENABLE_PIN, True)
        sleep(duration)
        GPIO.output(ENABLE_PIN, False)


    def foreward(self, power, duration):
        GPIO.output(FORWARD_PIN, True)
        GPIO.output(BACKWARD_PIN, False)
        self.run(power, duration)


    def backward(self, power, duration):
        GPIO.output(BACKWARD_PIN, True)
        GPIO.output(FORWARD_PIN, False)
        self.run(power, duration)


if __name__ == '__main__':
    wheel = Wheel()
    wheel.foreward(50, 2)



