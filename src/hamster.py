from lib.common import Battery, Gyro, LCD, Touch, Piezo, ticks_diff
import math


class Hamster:
    MAX_BRIGHTNESS = 100

    def __init__(self, lcd: LCD, touch: Touch, gyro: Gyro, piezo: Piezo, battery: Battery, now_ms: int, tick_ms: int):
        self.face = Face(lcd)
        self.touch = touch
        self.gyro = gyro
        self.player = PiezoPlayer(piezo, tick_ms)
        self.battery = battery
        self.freefall_started_at = 0

        # Initial state
        lcd.set_brightness(Hamster.MAX_BRIGHTNESS)
        self.player.play(now_ms, SOUND_HELLO)
    
    def tick(self, now_ms: int, tick: int):
        self._simulate(now_ms)
        self.player.next_tune(now_ms)
        self.face.draw_face(now_ms)

        battery_pcnt = self.battery.battery_pcnt()
        if tick % 100 == 0:
            self.face.draw_battery_status(battery_pcnt, self.battery.is_charging())
        
        self.face.show()
        self.last_tick_ms = now_ms
    
    def _simulate(self, now_ms: int):
        
        # Check gestures
        gesture = self.touch.get_gesture()
        if gesture == Touch.UP: # Up -> feed
            self.face.set_next_face("eating", now_ms, 1000, 1)
        elif gesture == Touch.DOWN: # Down -> pet
            self.face.set_next_face("content", now_ms, 1000, 1)
        
        # Check gyro
        ax, ay, az, gx, gy, gz = self.gyro.read_axyz_gxyz()
        if self.detect_drop(ax, ay, az, now_ms): # Dropped -> dead
            self.face.set_next_face("dead", now_ms, 60000, 10)
        elif self.detect_shake(ax, ay, az, gx, gy, gz): # Shaken -> scared
            self.player.play(now_ms, SOUND_EEEK)
            self.face.set_next_face("scared", now_ms, 2000, 5)
        elif self.detect_gentle(ax, ay, az, gx, gy, gz): # Gently moved -> happy
            self.face.set_next_face("happy", now_ms, 2000, 1)
    
    def detect_drop(self, ax: float, ay: float, az: float, now_ms: int) -> bool:
        mag2 = ax*ax + ay*ay + az*az
        print(f"Gyro[{now_ms}][{self.freefall_started_at}][{ticks_diff(now_ms, self.freefall_started_at)}]: {ax} {ay} {az} => {mag2}") # DEBUG
        if mag2 >= 1.5: # Hamster's falling
            if self.freefall_started_at == 0:
                self.freefall_started_at = now_ms
            return ticks_diff(now_ms, self.freefall_started_at) > 100 # Hamster's doomed
        self.freefall_started_at = 0
        return False

    BASELINE_A = 1.018      # 1.018 is a baseline computed while still, could determine it dynamically
    SHAKE_ACCEL_DEV = 0.15  # deviation from gravity (g)
    SHAKE_GYRO = 240        # deg/s
    GENTLE_DEV_MIN = 0.07    # just above noise

    def detect_shake(self, ax: float, ay: float, az: float, gx: float, gy: float, gz: float) -> bool:
        a = math.sqrt(ax*ax + ay*ay + az*az)
        dev = abs(a - Hamster.BASELINE_A)
        g = max(abs(gx), abs(gy), abs(gz))
        return dev > Hamster.SHAKE_ACCEL_DEV or g > Hamster.SHAKE_GYRO

    def detect_gentle(self, ax: float, ay: float, az: float, gx: float, gy: float, gz: float) -> bool:
        a = math.sqrt(ax*ax + ay*ay + az*az)
        dev = abs(a - Hamster.BASELINE_A)
        g = max(abs(gx), abs(gy), abs(gz))
        return Hamster.GENTLE_DEV_MIN < dev < Hamster.SHAKE_ACCEL_DEV and g < Hamster.SHAKE_GYRO

class PiezoPlayer:
    _BASE_FREQ = 8000 # Hz

    def __init__(self, piezo: Piezo, tick_ms: int):
        self.piezo = piezo
        self.tick_ms = tick_ms
        self.start_time = 0

    def play(self, now_ms: int, tune: bytes):
        """Sets the tune in the following format:
        freq_div [0-255]
        volume [0-100]
        at_tick [0-255]
        """
        self.tune = tune
        self.start_time = now_ms
        self.next_time = 0
        self.next_idx = 0

    def next_tune(self, current_time: int):
        i = self.next_idx
        while i < len(self.tune):
            freq_div = self.tune[i]
            volume = self.tune[i+1]
            at_tick = self.tune[i+2]
            i += 3

            if current_time >= self.next_time:
                self.piezo.beep(PiezoPlayer._BASE_FREQ // freq_div, volume)
                self.next_time = self.start_time + (at_tick * self.tick_ms)
                self.next_idx = i
                return
        self.piezo.beep(0, 0)

SOUND_HELLO = bytes((
    # freq_div, volume, at_tick
    16, 40, 0,    # He-
    14, 50, 30,   # -el
    12, 60, 60,   # short accent
    20, 30, 100,  # quick dip
    9,  70, 140,  # loooo! rising pitch
))

SOUND_EEEK = bytes((
    # freq_div, volume, at_tick
    3, 90, 50,    # EEEE!
))

class Face:
    def __init__(self, lcd: LCD):
        self.lcd = lcd
        self.start_at = 0
        self.reset_at = 0
        self.face_id = "default"
        self.current_priority = 0
    
    def set_next_face(self, face_id: str, now_ms: int, duration_ms: int, priority: int, delay_ms=0):
        if priority < self.current_priority:
            return
        
        self.start_at = now_ms + delay_ms
        self.reset_at = now_ms + delay_ms + duration_ms
        self.face_id = face_id
        self.current_priority = priority

    def draw_face(self, now_ms):
        if not self.face_id:
            return
        if now_ms >= self.reset_at:
            self._load_face("default")
            self.face_id = None
            self.current_priority = 0
        elif now_ms >= self.start_at:
            self._load_face(self.face_id)
    
    def draw_battery_status(self, battery_pcnt: int, is_charging: bool):
        if is_charging:
            self.lcd.fill_rect(0, 220-2, 240, 12+2, 0x000000)
            self.lcd.text(f"{battery_pcnt:.0f}%", 80, 220, 0xFFFFFF)
        else:
            self.lcd.set_brightness(int(Hamster.MAX_BRIGHTNESS * battery_pcnt / 100))

    def show(self):
        self.lcd.show()

    def _load_face(self, face_id: str):
        with open(f"/resources/hamster_240_{face_id}.rgb565", "rb") as f:
            f.readinto(self.lcd.buffer)
