from waveshare.LCD_1inch28 import LCD_1inch28
from waveshare.Touch_CST816T import Touch_CST816T
import time


LCD = LCD_1inch28()
LCD.set_bl_pwm(65535 * 60 // 100)

Touch=Touch_CST816T(mode=1,LCD=LCD)

Touch.Mode = 0
Touch.Set_Mode(Touch.Mode)

LCD.fill(LCD.white)
LCD.write_text('Gesture test',70,90,1,LCD.black)
LCD.show()

while True:
    if Touch.Gestures > 0:
        LCD.fill(LCD.white)
        
        if Touch.Gestures == 0x01:
            LCD.write_text('UP',100,110,3,LCD.black)
        elif Touch.Gestures == 0x02:
            LCD.write_text('DOWN',70,110,3,LCD.black)
        elif Touch.Gestures == 0x03:
            LCD.write_text('LEFT',70,110,3,LCD.black)
        elif Touch.Gestures == 0x04:
            LCD.write_text('RIGHT',70,110,3,LCD.black)
        elif Touch.Gestures == 0x0C:
            LCD.write_text('Long Press',40,110,2,LCD.black)
        elif Touch.Gestures == 0x0B:
            LCD.write_text('Double Click',25,110,2,LCD.black)
        
        LCD.show()
        time.sleep(1.0)
    else:
        time.sleep(0.1)
