from gpiozero import Motor
from gpiozero import OutputDevice
import time


RELAY_PIN = 23

#motors
motorLeft = Motor(14, 18)
motorRight = Motor(27, 22)

#paint dispenser
pumpRelay = OutputDevice(RELAY_PIN, active_high=True, initial_value=False)

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

def set_relay(status):
    if status:
        print("Setting relay: ON")
        pumpRelay.on()
    else:
        print("Setting relay: OFF")
        pumpRelay.off()

def paint(period=DEFAULT_PERIOD):
    set_relay(True)
    time.sleep(period)
    set_relay(False)

if __name__ == "__main__":
    while True:
        paint(5)
        time.sleep(5)
