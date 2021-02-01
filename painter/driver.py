from gpiozero import Motor
from gpiozero import OutputDevice
import time


RELAY_PIN = 21

#motors
motorLeft = Motor(26, 20)
motorRight = Motor(16, 19)

leftPowerFactor = 1.0
rightPowerFactor = 1.3

def limit(power):
    if power > 1.0:
        return 1.0
    elif power < -1.0:
        return -1.0
    else:
        return power

#paint dispenser
pumpRelay = OutputDevice(RELAY_PIN, active_high=True, initial_value=False)

DEFAULT_PWR = 0.3

def start_left(power=DEFAULT_PWR, paint=False):
    set_relay(paint)
    motorRight.forward(limit(power * rightPowerFactor))

def start_right(power=DEFAULT_PWR, paint=False):
    set_relay(paint)
    motorLeft.forward(limit(power * leftPowerFactor))

def forward(power=DEFAULT_PWR, paint=True):
    set_relay(paint)
    motorLeft.forward(limit(power * leftPowerFactor))
    motorRight.forward(limit(power * rightPowerFactor))

def stop_all():
    set_relay(False)
    motorLeft.stop()
    motorRight.stop()
    
def set_relay(status):
    if status:
        print("Setting relay: ON")
        pumpRelay.on()
    else:
        print("Setting relay: OFF")
        pumpRelay.off()

def paint(period=2):
    set_relay(True)
    time.sleep(period)
    set_relay(False)

if __name__ == "__main__":
    while True:
        paint(5)
        time.sleep(5)
