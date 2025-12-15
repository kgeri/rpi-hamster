from typing import Final, Protocol


class LCD(Protocol):
    buffer: bytearray

    def set_brightness(self, percentage: int):
        pass

    def show(self) -> None:
        pass

class Touch(Protocol):
    UP = 0x01
    DOWN = 0x02
    LEFT = 0x03
    RIGHT = 0x04
    DOUBLE_TAP = 0x0B
    LONG_PRESS = 0x0C

    gesture: int

class Gyro(Protocol):
    def read_axyz_gxyz(self) -> list[float]:
        pass

class Piezo(Protocol):
    def beep(self, freq: int, volume: int) -> None:
        pass
