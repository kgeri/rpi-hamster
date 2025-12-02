from lib.CST816T import Touch
from lib.LCD_1in28 import LCD_1in28
from lib.LVGL import LVGL
from machine import Pin
from utime import sleep


LCD = LCD_1in28()
LCD.set_bl_pwm(65535 * 60 // 100)
print("Init LCD done")

# Init Touch
TSC = Touch(mode=2,LCD=LCD)
print("Init TSC done")

LVGL(LCD=LCD,TSC=TSC)
print("Init LVGL done")

pin = Pin("LED", Pin.OUT)

print("LED starts flashing...")
while True:
    try:
        pin.toggle()
        sleep(1) # sleep 1sec
    except KeyboardInterrupt:
        break
pin.off()
print("Finished.")
