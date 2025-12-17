from hamster import Hamster
from lib.waveshare import Battery_WS_RP2350, Gyro_QMI8658, LCD_GC9A01A, Piezo_WS_RP2350, Touch_CST816T
import sys
import time


TICK_MS = 10

try:
    hs = Hamster(
        LCD_GC9A01A(), 
        Touch_CST816T(),
        Gyro_QMI8658(),
        Piezo_WS_RP2350(),
        Battery_WS_RP2350(),
        time.ticks_ms(),
        TICK_MS
    )
    while True:
        hs.tick(time.ticks_ms())
        time.sleep_ms(TICK_MS)
except Exception as e:
    sys.print_exception(e)
