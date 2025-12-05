from lib.LCD_1inch28 import LCD_1inch28
from lib.QMI8658 import QMI8658
import time, math


LCD = LCD_1inch28()
LCD.set_bl_pwm(65535 * 60 // 100)


FREEFALL_G = 0.25  # threshold in g
FREEFALL_TIME = 0.03  # 30 ms

ff_timer = 0.0

def detect_drop(ax, ay, az, dt):
    global ff_timer

    a = math.sqrt(ax*ax + ay*ay + az*az)

    if a < FREEFALL_G:       # near zero-g
        ff_timer += dt
        if ff_timer > FREEFALL_TIME:
            ff_timer = 0
            return True
    else:
        ff_timer = 0

    return False

SHAKE_ACCEL_DEV = 0.15   # deviation from gravity (g)
SHAKE_GYRO = 240         # deg/s

# optional: compute baseline once while still
BASELINE_A = 1.018

def detect_shake(ax, ay, az, gx, gy, gz):
    a = math.sqrt(ax*ax + ay*ay + az*az)
    dev = abs(a - BASELINE_A)
    g = max(abs(gx), abs(gy), abs(gz))

    return dev > SHAKE_ACCEL_DEV or g > SHAKE_GYRO

GENTLE_DEV_MIN = 0.07    # just above noise

def detect_gentle(ax, ay, az, gx, gy, gz):
    a = math.sqrt(ax*ax + ay*ay + az*az)
    dev = abs(a - BASELINE_A)
    g = max(abs(gx), abs(gy), abs(gz))

    return GENTLE_DEV_MIN < dev < SHAKE_ACCEL_DEV and g < SHAKE_GYRO


qmi8658=QMI8658()
last = time.ticks_ms()
no_check_till = 0
emote = ''
while True:
    xyz=qmi8658.Read_XYZ()
    ax, ay, az = xyz[:3]
    gx, gy, gz = xyz[3:]

    print(f'{ax}, {ay}, {az} | {gz}, {gy}, {gz}')

    now = time.ticks_ms()
    dt = time.ticks_diff(now, last) / 1000
    last = now

    LCD.fill(LCD.black)
    LCD.text(f'{ax:+.2f},{ay:+.2f},{az:+.2f}',20,80-3,LCD.white)
    LCD.text(f'{gx:+.2f},{gy:+.2f},{gz:+.2f}',20,90-3,LCD.white)

    if now > no_check_till:
        if detect_drop(ax, ay, az, dt):
            emote = 'OUCH!!'
            no_check_till = now + 1000
        elif detect_shake(ax, ay, az, gx, gy, gz):
            emote = 'AAAA!!'
            no_check_till = now + 1000
        elif detect_gentle(ax, ay, az, gx, gy, gz):
            emote = 'WHEEE!'
            no_check_till = now + 1000
        else:
            emote = ''
    LCD.write_text(emote,70,110,3,LCD.white)
    
    LCD.show()
    time.sleep_ms(10)
