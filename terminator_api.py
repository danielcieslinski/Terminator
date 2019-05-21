import RPi.GPIO as GPIO
from time import sleep
import threading



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
        ths = [threading.Thread(target=line.forward, args=(duration,)) for line in [self.left_wheels, self.right_wheels] ]
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
        self.sensor_type = type
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

if __name__ == '__main__':

    # sensor = Sensor()
    #
    # try: oas.loop()
    # except: GPIO.cleanup()

    vehicle = Vehicle([16,18], [38,40])
    vehicle.forward(5)

    GPIO.cleanup()
