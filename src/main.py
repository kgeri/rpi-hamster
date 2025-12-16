from hamster import HamsterSimulator
from lib.waveshare import Battery_WS_RP2350, Gyro_QMI8658, LCD_GC9A01A, Piezo_WS_RP2350, Touch_CST816T
import sys


try:
    HamsterSimulator(
        LCD_GC9A01A(), 
        Touch_CST816T(),
        Gyro_QMI8658(),
        Piezo_WS_RP2350(),
        Battery_WS_RP2350()
    ).loop()
except Exception as e:
    sys.print_exception(e)
