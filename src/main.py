from lib.LCD_1inch28 import LCD_1inch28


with open("/resources/hamster_main.rgb565", "rb") as f:
    hamster = f.read()

LCD = LCD_1inch28()
LCD.set_bl_pwm(65535 * 60 // 100)
LCD.buffer = hamster

LCD.show()
