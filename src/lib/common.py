
class LCD:
    buffer: bytearray

    def set_brightness(self, percentage: int):
        """Set screen brightness, 0-100"""
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

    gesture: int
    """Direction of the gesture"""

class Gyro:

    def read_axyz_gxyz(self) -> list[int]:
        """Returns acceleration (x, y, z) and gyroscopic acceleration (x, y, z)"""
        raise NotImplementedError

class Piezo:

    def beep(self, freq: int, volume: int) -> None:
        """Sets the frequency (in Hz) and volume (0-100) of the piezo"""
        raise NotImplementedError
