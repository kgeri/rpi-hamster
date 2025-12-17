from lib.common import Battery, Gyro, LCD, Touch, Piezo
import math


class Hamster:
    def __init__(self, lcd: LCD, touch: Touch, gyro: Gyro, piezo: Piezo, battery: Battery, now_ms: int, tick_ms: int):
        self.face = Face(lcd, battery)
        self.touch = touch
        self.gyro = gyro
        self.player = PiezoPlayer(piezo, tick_ms)

        self.freefall_started_at = 0

        # Initial state
        lcd.set_brightness(60)
        self.player.play(now_ms, SOUND_HELLO)
    
    def tick(self, now_ms: int):
        self._simulate(now_ms)
        self.player.next_tune(now_ms)
        self.face.draw_face(now_ms)
        self.face.draw_battery_status()
        self.face.show()
        self.last_tick_ms = now_ms
    
    def _simulate(self, now_ms: int):
        
        # Check gestures
        gesture = self.touch.gesture
        if gesture == Touch.UP: # Up -> feed
            self.face.set_next_face("eating", now_ms, 1000)
        elif gesture == Touch.DOWN: # Down -> pet
            self.face.set_next_face("cotnent", now_ms, 1000)
        
        # Check gyro
        ax, ay, az, gx, gy, gz = self.gyro.read_axyz_gxyz()
        if self.detect_drop(ax, ay, az, now_ms): # Dropped -> dead
            self.face.set_next_face("dead", now_ms, 60000, override=True)
        elif self.detect_shake(ax, ay, az, gx, gy, gz): # Shaken -> scared
            self.player.play(now_ms, SOUND_EEEK)
            self.face.set_next_face("scared", now_ms, 2000, override=True)
        elif self.detect_gentle(ax, ay, az, gx, gy, gz): # Gently moved -> happy
            self.face.set_next_face("happy", now_ms, 2000)
    
    def detect_drop(self, ax: float, ay: float, az: float, now_ms: int) -> bool:
        mag2 = ax*ax + ay*ay + az*az
        if mag2 >= 0.25: # >= (0.5g)^2 -> not freefall
            self.freefall_started_at = 0
            return False
        elif not self.freefall_started_at: # Freefall just started
            self.freefall_started_at = now_ms
            return False
        elif now_ms - self.freefall_started_at < 30: # Freefalling but not enough yet
            return False
        else:
            self.freefall_started_at = 0 # Hamster's doomed
            return True

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
    def __init__(self, lcd: LCD, battery: Battery):
        self.lcd = lcd
        self.battery = battery
        self.start_at = 0
        self.reset_at = 0
        self.face_id = "default"
    
    def set_next_face(self, face_id: str, now_ms: int, duration_ms: int, override=False, delay_ms = 0):
        if not override and now_ms < self.reset_at:
            return # Previous face still showing
        
        self.start_at = now_ms + delay_ms
        self.reset_at = now_ms + delay_ms + duration_ms
        self.face_id = face_id

    def draw_face(self, now_ms):
        if not self.face_id:
            return
        if now_ms >= self.reset_at:
            self._load_face("default")
            self.face_id = None
        elif now_ms >= self.start_at:
            self._load_face(self.face_id)
    
    def draw_battery_status(self):
        v = self.battery.read_voltage()
        b = self.battery.battery_pcnt()
        text = f"USB ({v:.2f}V)" if self.battery.is_charging() else f"{b}% ({v:.2f}V)"
        self.lcd.fill_rect(0, 220-2, 240, 12+2, 0x00FF00)
        self.lcd.text(text, 80, 220, 0xFFFFFF)

    def show(self):
        self.lcd.show()

    def _load_face(self, face_id: str):
        with open(f"/resources/hamster_240_{face_id}.rgb565", "rb") as f:
            f.readinto(self.lcd.buffer)
