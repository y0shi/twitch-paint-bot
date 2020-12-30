from gpiozero import Motor
import time

motorLeft = Motor(4, 14)
motorRight = Motor(17, 27)

DEFAULT_PWR = 0.5
DEFAULT_PERIOD = 2

def turn_left(power=DEFAULT_PWR, period=DEFAULT_PERIOD):
    motorRight.forward(power)
    time.sleep(period)
    motorRight.stop()

def turn_right(power=DEFAULT_PWR, period=DEFAULT_PERIOD):
    motorLeft.forward(power)
    time.sleep(period)
    motorLeft.stop()

def forward(power=DEFAULT_PWR, period=DEFAULT_PERIOD):
    motorLeft.forward(power)
    motorRight.forward(power)
    time.sleep(period)
    motorLeft.stop()
    motorRight.stop()

if __name__ == "__main__":
    turn_left()
    turn_right()
    forward()

