from hamster import HamsterSimulator
from lib.waveshare import Gyro_QMI8658, LCD_WS_RP2350, Piezo_WS_RP2350, Touch_CST816T
import sys


try:
    HamsterSimulator(
        LCD_WS_RP2350(), 
        Touch_CST816T(),
        Gyro_QMI8658(),
        Piezo_WS_RP2350()
    ).loop()
except Exception as e:
    sys.print_exception(e)
