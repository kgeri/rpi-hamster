from typing import Final, Protocol


class LCD(Protocol):
    buffer: bytearray

    def set_brightness(self, percentage: int):
        pass

    def text(self, s: str, x: int, y: int, c: int = 1, /) -> None:
        pass

    def fill_rect(self, *args, **kwargs):
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

    def get_gesture(self) -> int:
        pass

class Gyro(Protocol):
    def read_axyz_gxyz(self) -> list[float]:
        pass

class Piezo(Protocol):
    def beep(self, freq: int, volume: int) -> None:
        pass

class Battery(Protocol):
    def read_voltage(self) -> float:
        pass

    def battery_pcnt(self) -> int:
        pass

    def is_charging(self) -> bool:
        pass
