from waveshare.LCD_1inch28 import LCD_1inch28
import time


LCD = LCD_1inch28()
LCD.set_bl_pwm(65535 * 60 // 100)

def show_frame(frame_name, delay_ms=1000):
    with open(f"/resources/{frame_name}.rgb565", "rb") as f:
        f.readinto(LCD.buffer)
    LCD.show()
    time.sleep_ms(delay_ms)

while True:
    show_frame('hamster_240_default')
    show_frame('hamster_240_content')
    show_frame('hamster_240_happy')
    show_frame('hamster_240_scared')
    show_frame('hamster_240_sick')
    show_frame('hamster_240_dead')
