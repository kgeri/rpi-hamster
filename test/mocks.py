from lib.common import LCD, Touch, Gyro, Piezo, Battery


class MockLCD(LCD):
    def __init__(self):
        self.buffer = bytearray(240 * 240 * 2)

    def set_brightness(self, percentage: int):
        pass

    def text(self, s: str, x: int, y: int, c: int = 1, /) -> None:
        pass

    def fill_rect(self, *args, **kwargs):
        pass

    def show(self) -> None:
        pass


class MockTouch(Touch):
    UP = 0x01
    DOWN = 0x02
    LEFT = 0x03
    RIGHT = 0x04
    DOUBLE_TAP = 0x0B
    LONG_PRESS = 0x0C

    def __init__(self):
        self._gesture = 0

    def get_gesture(self) -> int:
        g = self._gesture
        self._gesture = 0
        return g


class MockGyro(Gyro):
    def __init__(self):
        self._values = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]

    def read_axyz_gxyz(self) -> list[float]:
        return self._values


class MockPiezo(Piezo):
    def beep(self, freq: int, volume: int) -> None:
        pass


class MockBattery(Battery):
    def battery_pcnt(self) -> int:
        return 100

    def is_charging(self) -> bool:
        return False
