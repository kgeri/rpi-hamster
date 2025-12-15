from waveshare.LCD_1inch28 import LCD_1inch28
from waveshare.QMI8658 import QMI8658
from waveshare.Touch_CST816T import Touch_CST816T
from machine import ADC, PWM, Pin
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

def show_frame(frame_name):
    with open(f"/resources/hamster_240_{frame_name}.rgb565", "rb") as f:
        f.readinto(LCD.buffer)
    LCD.show()

# Sound - TODO move to lib
piezo = PWM(Pin(16))    # GP15 is fine
def beep(freq, ms):
    piezo.freq(freq)
    piezo.duty_u16(30000)   # loudness (0 - 65535)
    time.sleep_ms(ms)
    piezo.duty_u16(0)   # stop

qmi8658=QMI8658()

Touch=Touch_CST816T(mode=1,LCD=LCD)
Touch.Mode = 0
Touch.Set_Mode(Touch.Mode)

# Battery voltage
PIN_VBAT = 29
Vbat= ADC(Pin(PIN_VBAT))
v_bat = Vbat.read_u16()*3.3/65535 * 3

print(f'Booted successfully, Vbat={v_bat:.2f}V')
beep(2000, 200)

last = time.ticks_ms()
no_draw_till = 0
emote = ''
emote_before = ''
while True:
    xyz=qmi8658.Read_XYZ()
    ax, ay, az = xyz[:3]
    gx, gy, gz = xyz[3:]

    now = time.ticks_ms()
    dt = time.ticks_diff(now, last) / 1000
    last = now

    if Touch.Gestures == 0x01: # Up = feed
        emote = 'eating'
        Touch.Gestures = 0
    elif Touch.Gestures == 0x02: # Down = pet
        emote = 'content'
        Touch.Gestures = 0
    elif detect_drop(ax, ay, az, dt):
        emote = 'dead'
    elif detect_shake(ax, ay, az, gx, gy, gz):
        emote = 'scared'
    elif detect_gentle(ax, ay, az, gx, gy, gz):
        emote = 'happy'
    else:
        emote = 'default'
    
    if emote_before != emote and now > no_draw_till:
        show_frame(emote)
        emote_before = emote
        if emote == 'dead':
            no_draw_till = now + 60000
        elif emote == 'eating':
            no_draw_till = now + 2000
            beep(1000, 500)
        elif emote == 'scared':
            no_draw_till = now + 2000
            beep(3000, 500)
        else:
            no_draw_till = now + 1000
    time.sleep_ms(10)
