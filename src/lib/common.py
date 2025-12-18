
class LCD:
    buffer: bytearray

    def set_brightness(self, percentage: int):
        """Set screen brightness, 0-100"""
        raise NotImplementedError

    def text(self, s: str, x: int, y: int, c: int = 1):
        raise NotImplementedError

    def fill_rect(self, *args, **kwargs):
        raise NotImplementedError

    def show(self) -> None:
        """Shows the contents of the buffer on screen"""
        raise NotImplementedError

class Touch:
    UP = 0x01
    DOWN = 0x02
    LEFT = 0x03
    RIGHT = 0x04
    DOUBLE_TAP = 0x0B
    LONG_PRESS = 0x0C

    def get_gesture(self) -> int:
        """Direction of the gesture"""
        raise NotImplementedError

class Gyro:
    def read_axyz_gxyz(self) -> list[int]:
        """Returns acceleration (x, y, z) and gyroscopic acceleration (x, y, z)"""
        raise NotImplementedError

class Piezo:
    def beep(self, freq: int, volume: int) -> None:
        """Sets the frequency (in Hz) and volume (0-100) of the piezo"""
        raise NotImplementedError

class Battery:
    def read_voltage(self) -> float:
        """Returns the measured battery or USB rail voltage"""
        raise NotImplementedError

    def battery_pcnt(self) -> int:
        """Returns the estimated battery percentage (0-100)"""
        raise NotImplementedError
    
    def is_charging(self) -> bool:
        raise NotImplementedError
