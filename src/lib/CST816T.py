from machine import Pin, I2C
import time

# Pin definition  
I2C_SDA = 6
I2C_SDL = 7
I2C_IRQ = 21 
I2C_RST = 22

# Touch drive 
class Touch(object):
    # Initialize the touch chip 
    def __init__(self,address=0x15,mode=0,i2c_num=1,i2c_sda=I2C_SDA,i2c_scl=I2C_SDL,irq_pin=I2C_IRQ,rst_pin=I2C_RST,LCD=None):
        self._bus = I2C(id=i2c_num,scl=Pin(i2c_scl),sda=Pin(i2c_sda),freq=100_000) # Initialize I2C
        self._address = address # Set slave address  
        self.int=Pin(irq_pin,Pin.IN, Pin.PULL_UP)         
        self.rst=Pin(rst_pin,Pin.OUT)
        self.Reset()
        bRet=self.WhoAmI()
        if bRet :
            self.Stop_Sleep()
        else    :
            print("Error: Not Detected CST816D.")
            return None
        self.Mode = mode
        self.Gestures="None"
        self.Flag = self.Flgh =self.l = 0
        self.X_point = self.Y_point = 0
        self.int.irq(handler=self.Int_Callback,trigger=Pin.IRQ_FALLING)
      
    def _read_byte(self,cmd):
        rec=self._bus.readfrom_mem(int(self._address),int(cmd),1)
        return rec[0]
    
    def _read_block(self, reg, length=1):
        rec=self._bus.readfrom_mem(int(self._address),int(reg),length)
        return rec
    
    def _write_byte(self,cmd,val):
        self._bus.writeto_mem(int(self._address),int(cmd),bytes([int(val)]))

    def WhoAmI(self):
        if (0xB5) != self._read_byte(0xA7):
            return False
        return True
    
    def Read_Revision(self):
        return self._read_byte(0xA9)
      
    # Stop sleeping  
    def Stop_Sleep(self):
        self._write_byte(0xFE,0x01)
    
    # Reset     
    def Reset(self):
        self.rst(0)
        time.sleep_ms(1)
        self.rst(1)
        time.sleep_ms(50)
    
    # Set mode    
    def Set_Mode(self,mode,callback_time=10,rest_time=5): 
        # mode = 0 gestures mode 
        # mode = 1 point mode 
        # mode = 2 mixed mode 
        if (mode == 1):      
            self._write_byte(0xFA,0X41)
            
        elif (mode == 2) :
            self._write_byte(0xFA,0X71)
            
        else:
            self._write_byte(0xFA,0X11)
            self._write_byte(0xEC,0X01)
     
    # Get the coordinates of the touch  
    def get_point(self):
        xy_point = self._read_block(0x03,4)
        
        x_point= ((xy_point[0]&0x0f)<<8)+xy_point[1]
        y_point= ((xy_point[2]&0x0f)<<8)+xy_point[3]
        
        self.X_point=x_point
        self.Y_point=y_point
        
    def get_gestures(self):
        self.Gestures = self._read_byte(0x01)
        
    def Int_Callback(self,pin):
        if self.Mode == 0 :
            self.Gestures = self._read_byte(0x01)

        elif self.Mode == 1 :           
            self.Flag = 1
            self.get_point()
        
        elif self.Mode == 2 :           
            self.Flag = 1
            self.get_point()
            self.Gestures = self._read_byte(0x01)

    def Timer_callback(self,t):
        self.l += 1
        if self.l > 100:
            self.l = 50
            