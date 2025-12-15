from waveshare.CST816T import Touch
from waveshare.LCD_1in28 import LCD_1in28
from waveshare.LVGL import LVGL
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


import lvgl as lv

W = 240
H = 240

# Allocate RAM buffer
buf = bytearray(W * H * 2)

# Load raw RGB565 file into buffer
with open("/resources/hamster_main.rgb565", "rb") as f:
    f.readinto(buf)

scr = lv.obj()

# Create a canvas using RGB565
canvas = lv.canvas(scr)
canvas.set_buffer(buf, W, H, lv.COLOR_FORMAT.RGB565)
canvas.center()

lv.screen_load(scr)
