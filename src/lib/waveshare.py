# Source: https://files.waveshare.com/wiki/RP2350-Touch-LCD-1.28/RP2350-Touch-LCD-1.28.zip
# Code and docs cleaned up

from framebuf import FrameBuffer, RGB565
from lib.logging import LOG
from machine import ADC, I2C, Pin, PWM, SPI
import time


class LCD_GC9A01A(FrameBuffer):
    """Round LCD, 1.28 inch, touch-capable"""

    def __init__(self): # SPI initialization
        self.width = 240
        self.height = 240
        
        self.cs = Pin(9, Pin.OUT)
        self.rst = Pin(13, Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1,100_000_000, polarity=0, phase=0, bits=8, sck=Pin(10), mosi=Pin(11), miso=None)
        self.dc = Pin(8, Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, RGB565)
        self._init_display()
        
        # Define color, Micropython fixed to BRG format
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        self.brown =   0X8430
        
        self.fill(self.white) # Clear screen
        self.show() # Show

        self.pwm = PWM(Pin(25))
        self.pwm.freq(5000) #Turn on the backlight

    def set_brightness(self, percentage: int):
        """Set screen brightness, max 65535"""
        self.pwm.duty_u16(65535 * percentage // 100)
    
    def show(self):
        """Shows the contents of the buffer on screen"""
        self._set_windows(0,0,self.width,self.height)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

    def _write_cmd(self, cmd): # Write command
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def _write_data(self, buf): # Write data
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def _init_display(self):
        """LCD initialization"""  
        self.rst(1)
        time.sleep(0.01)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        time.sleep(0.05)
        
        self._write_cmd(0xEF)
        self._write_cmd(0xEB)
        self._write_data(0x14) 
        
        self._write_cmd(0xFE) 
        self._write_cmd(0xEF) 

        self._write_cmd(0xEB)
        self._write_data(0x14) 

        self._write_cmd(0x84)
        self._write_data(0x40) 

        self._write_cmd(0x85)
        self._write_data(0xFF) 

        self._write_cmd(0x86)
        self._write_data(0xFF) 

        self._write_cmd(0x87)
        self._write_data(0xFF)

        self._write_cmd(0x88)
        self._write_data(0x0A)

        self._write_cmd(0x89)
        self._write_data(0x21) 

        self._write_cmd(0x8A)
        self._write_data(0x00) 

        self._write_cmd(0x8B)
        self._write_data(0x80) 

        self._write_cmd(0x8C)
        self._write_data(0x01) 

        self._write_cmd(0x8D)
        self._write_data(0x01) 

        self._write_cmd(0x8E)
        self._write_data(0xFF) 

        self._write_cmd(0x8F)
        self._write_data(0xFF) 


        self._write_cmd(0xB6)
        self._write_data(0x00)
        self._write_data(0x20)

        self._write_cmd(0x36)
        self._write_data(0x98)

        self._write_cmd(0x3A)
        self._write_data(0x05) 


        self._write_cmd(0x90)
        self._write_data(0x08)
        self._write_data(0x08)
        self._write_data(0x08)
        self._write_data(0x08) 

        self._write_cmd(0xBD)
        self._write_data(0x06)
        
        self._write_cmd(0xBC)
        self._write_data(0x00)

        self._write_cmd(0xFF)
        self._write_data(0x60)
        self._write_data(0x01)
        self._write_data(0x04)

        self._write_cmd(0xC3)
        self._write_data(0x13)
        self._write_cmd(0xC4)
        self._write_data(0x13)

        self._write_cmd(0xC9)
        self._write_data(0x22)

        self._write_cmd(0xBE)
        self._write_data(0x11) 

        self._write_cmd(0xE1)
        self._write_data(0x10)
        self._write_data(0x0E)

        self._write_cmd(0xDF)
        self._write_data(0x21)
        self._write_data(0x0c)
        self._write_data(0x02)

        self._write_cmd(0xF0)   
        self._write_data(0x45)
        self._write_data(0x09)
        self._write_data(0x08)
        self._write_data(0x08)
        self._write_data(0x26)
        self._write_data(0x2A)

        self._write_cmd(0xF1)    
        self._write_data(0x43)
        self._write_data(0x70)
        self._write_data(0x72)
        self._write_data(0x36)
        self._write_data(0x37)  
        self._write_data(0x6F)


        self._write_cmd(0xF2)   
        self._write_data(0x45)
        self._write_data(0x09)
        self._write_data(0x08)
        self._write_data(0x08)
        self._write_data(0x26)
        self._write_data(0x2A)

        self._write_cmd(0xF3)   
        self._write_data(0x43)
        self._write_data(0x70)
        self._write_data(0x72)
        self._write_data(0x36)
        self._write_data(0x37) 
        self._write_data(0x6F)

        self._write_cmd(0xED)
        self._write_data(0x1B) 
        self._write_data(0x0B) 

        self._write_cmd(0xAE)
        self._write_data(0x77)
        
        self._write_cmd(0xCD)
        self._write_data(0x63)


        self._write_cmd(0x70)
        self._write_data(0x07)
        self._write_data(0x07)
        self._write_data(0x04)
        self._write_data(0x0E) 
        self._write_data(0x0F) 
        self._write_data(0x09)
        self._write_data(0x07)
        self._write_data(0x08)
        self._write_data(0x03)

        self._write_cmd(0xE8)
        self._write_data(0x34)

        self._write_cmd(0x62)
        self._write_data(0x18)
        self._write_data(0x0D)
        self._write_data(0x71)
        self._write_data(0xED)
        self._write_data(0x70) 
        self._write_data(0x70)
        self._write_data(0x18)
        self._write_data(0x0F)
        self._write_data(0x71)
        self._write_data(0xEF)
        self._write_data(0x70) 
        self._write_data(0x70)

        self._write_cmd(0x63)
        self._write_data(0x18)
        self._write_data(0x11)
        self._write_data(0x71)
        self._write_data(0xF1)
        self._write_data(0x70) 
        self._write_data(0x70)
        self._write_data(0x18)
        self._write_data(0x13)
        self._write_data(0x71)
        self._write_data(0xF3)
        self._write_data(0x70) 
        self._write_data(0x70)

        self._write_cmd(0x64)
        self._write_data(0x28)
        self._write_data(0x29)
        self._write_data(0xF1)
        self._write_data(0x01)
        self._write_data(0xF1)
        self._write_data(0x00)
        self._write_data(0x07)

        self._write_cmd(0x66)
        self._write_data(0x3C)
        self._write_data(0x00)
        self._write_data(0xCD)
        self._write_data(0x67)
        self._write_data(0x45)
        self._write_data(0x45)
        self._write_data(0x10)
        self._write_data(0x00)
        self._write_data(0x00)
        self._write_data(0x00)

        self._write_cmd(0x67)
        self._write_data(0x00)
        self._write_data(0x3C)
        self._write_data(0x00)
        self._write_data(0x00)
        self._write_data(0x00)
        self._write_data(0x01)
        self._write_data(0x54)
        self._write_data(0x10)
        self._write_data(0x32)
        self._write_data(0x98)

        self._write_cmd(0x74)
        self._write_data(0x10)
        self._write_data(0x85)
        self._write_data(0x80)
        self._write_data(0x00) 
        self._write_data(0x00) 
        self._write_data(0x4E)
        self._write_data(0x00)
        
        self._write_cmd(0x98)
        self._write_data(0x3e)
        self._write_data(0x07)

        self._write_cmd(0x35)
        self._write_cmd(0x21)

        self._write_cmd(0x11)

        self._write_cmd(0x29)
    
    def _set_windows(self,x1,y1,x2,y2): 
        self._write_cmd(0x2A)
        self._write_data(0x00)
        self._write_data(x1)
        self._write_data(0x00)
        self._write_data(x2-1)
        
        self._write_cmd(0x2B)
        self._write_data(0x00)
        self._write_data(y1)
        self._write_data(0x00)
        self._write_data(y2-1)
        
        self._write_cmd(0x2C)

class Touch_CST816T:
    """Touch sensor of the 1.28 inch LCD"""

    def __init__(self):
        self._bus = I2C(id=1, scl=Pin(7), sda=Pin(6), freq=400_000) # Initialize I2C
        self._address = 0x15 # Set slave address
        self.int = Pin(21, Pin.IN, Pin.PULL_UP)
        self.rst = Pin(22, Pin.OUT)
        self._reset()
        
        if (0xB5) != self._read_byte(0xA7):
            raise RuntimeError("Not Detected CST816T chip")
        
        self.gesture = 0
        self.int.irq(handler=self._int_callback, trigger=Pin.IRQ_FALLING)

        # Setting Gestures mode 
        self._write_byte(0xFA,0X11)
        self._write_byte(0xEC,0X01)
    
    def get_gesture(self) -> int:
        gesture = self.gesture
        self.gesture = 0
        return gesture

    def _read_byte(self,cmd) -> int:
        rec = self._bus.readfrom_mem(self._address, int(cmd), 1)
        return rec[0]

    def _write_byte(self,cmd,val) -> None:
        self._bus.writeto_mem(self._address, int(cmd), bytes([int(val)]))

    def _reset(self) -> None:
        self.rst(0)
        time.sleep_ms(1)
        self.rst(1)
        time.sleep_ms(50)
    
    def _int_callback(self, pin):
        self.gesture = self._read_byte(0x01)

class Gyro_QMI8658:
    """Gyro sensor built into the WS-2350"""
    _ADDRESS = 0X6B
    _ACC_LSB_DIV = (1<<12) # QMI8658AccRange_8g
    _GYRO_LSB_DIV = 64 # QMI8658GyrRange_512dps

    def __init__(self):
        self._bus = I2C(id=1, scl=Pin(7), sda=Pin(6), freq=100_000)
        
        if (0x05) != self._read_byte(0x00):
            raise RuntimeError("Not Detected QMI8658 chip")
        
        self._init_gyro()

    def read_axyz_gxyz(self) -> list[float]:
        xyz=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        try:
            raw_xyz=self._read_raw_xyz()
            for i in range(3):
                xyz[i] = raw_xyz[i] / Gyro_QMI8658._ACC_LSB_DIV
                xyz[i+3] = raw_xyz[i+3] / Gyro_QMI8658._GYRO_LSB_DIV
        except OSError as e:
            LOG.write("[QMI8658] Failed to read gyro: ", e)
        return xyz

    def _init_gyro(self):
        # REG CTRL1
        self._write_byte(0x02,0x60)
        # REG CTRL2 : QMI8658AccRange_8g and QMI8658AccOdr_1000Hz
        self._write_byte(0x03,0x23)
        # REG CTRL3 : QMI8658GyrRange_512dps and QMI8658GyrOdr_1000Hz
        self._write_byte(0x04,0x53)
        # REG CTRL4 : No
        self._write_byte(0x05,0x00)
        # REG CTRL5 : Enable Gyroscope And Accelerometer Low-Pass Filter 
        self._write_byte(0x06,0x11)
        # REG CTRL6 : Disables Motion on Demand.
        self._write_byte(0x07,0x00)
        # REG CTRL7 : Enable Gyroscope And Accelerometer
        self._write_byte(0x08,0x03)

    def _read_byte(self,cmd) -> int:
        rec=self._bus.readfrom_mem(Gyro_QMI8658._ADDRESS, int(cmd),1)
        return rec[0]

    def _read_block(self, reg, length=1) -> bytes:
        rec=self._bus.readfrom_mem(Gyro_QMI8658._ADDRESS, int(reg),length)
        return rec

    def _write_byte(self,cmd,val) -> None:
        self._bus.writeto_mem(Gyro_QMI8658._ADDRESS, int(cmd), bytes([int(val)]))

    def _read_raw_xyz(self) -> list[int]:
        xyz=[0,0,0,0,0,0]
        # raw_timestamp = self._read_block(0x30,3)
        # timestamp = (raw_timestamp[2]<<16)|(raw_timestamp[1]<<8)|(raw_timestamp[0])
        raw_xyz = self._read_block(0x35,12)
        for i in range(6):
            xyz[i] = (raw_xyz[(i*2)+1]<<8)|(raw_xyz[i*2])
            if xyz[i] >= 32767:
                xyz[i] = xyz[i]-65535
        return xyz

class Piezo_WS_RP2350:
    """A simple piezo I added to WS-2350"""

    def __init__(self):
        self.piezo = PWM(Pin(16))

    def beep(self, freq: int, volume: int):
        self.piezo.freq(freq)
        self.piezo.duty_u16(65535 * volume // 100) # loudness (0 - 65535)

class Battery_WS_RP2350:
    """Battery status for WS-2350"""
    # Lowest / highest voltages I measured on my PC (this should vary depending on the port/cable/etc.)
    _USB_LOW = 4.24
    _USB_HIGH = 4.61
    # Lowest / highest voltages I've measured with Akyga AKY0081
    _BATTERY_LOW = 3.28
    _BATTERY_HIGH = 3.99

    def __init__(self):
        self.vbat_adc = ADC(Pin(29))

    def read_voltage(self) -> float:
        return self.vbat_adc.read_u16() * 3.3 / 65535 * 3

    def battery_pcnt(self) -> int:
        v = self.read_voltage()
        if v >= Battery_WS_RP2350._USB_LOW and v > Battery_WS_RP2350._BATTERY_HIGH:
            return int((v - Battery_WS_RP2350._USB_LOW) * 100 / (Battery_WS_RP2350._USB_HIGH - Battery_WS_RP2350._USB_LOW))
        else:
            return int((v - Battery_WS_RP2350._BATTERY_LOW) * 100 / (Battery_WS_RP2350._BATTERY_HIGH - Battery_WS_RP2350._BATTERY_LOW))

    def is_charging(self) -> bool:
        v = self.read_voltage()
        # This is not documented, but testing shows that GPIO29 measures the USB rail when it's connected, and the battery voltage otherwise
        return v >= Battery_WS_RP2350._USB_LOW
