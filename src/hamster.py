from lib.common import Battery, Gyro, LCD, Touch, Piezo
import math
import time


TICK_MS = 10

class HamsterSimulator:
    def __init__(self, lcd: LCD, touch: Touch, gyro: Gyro, piezo: Piezo, battery: Battery):
        self.hamster = Hamster(lcd, touch, gyro, piezo, battery)
    
    def loop(self):
        last = time.ticks_ms()
        while True:
            now = time.ticks_ms()
            dt_ms = time.ticks_diff(now, last)
            
            self.hamster.simulate(dt_ms)
            self.hamster.player.next_tune(now)
            self.hamster.face.draw_face(now)
            self.hamster.face.draw_battery_status()
            self.hamster.face.show()
            
            last = now
            time.sleep_ms(TICK_MS)

class PiezoPlayer:
    _BASE_FREQ = 8000 # Hz

    def __init__(self, piezo: Piezo):
        self.piezo = piezo
        self.start_time = 0

    def play(self, tune: bytes):
        """Sets the tune in the following format:
        freq_div [0-255]
        volume [0-100]
        at_tick [0-255]
        """
        self.tune = tune
        self.start_time = time.ticks_ms()
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
                self.next_time = self.start_time + (at_tick * TICK_MS)
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
    
    def set_next_face(self, face_id: str, duration_ms, override=False, delay_ms = 0):
        now = time.ticks_ms()
        if not override and now < self.reset_at:
            return # Previous face still showing
        
        self.start_at = now + delay_ms
        self.reset_at = now + delay_ms + duration_ms
        self.face_id = face_id

    def draw_face(self, current_time):
        if not self.face_id:
            return
        if current_time >= self.reset_at:
            self._load_face("default")
            self.face_id = None
        elif current_time >= self.start_at:
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

class Hamster:
    def __init__(self, lcd: LCD, touch: Touch, gyro: Gyro, piezo: Piezo, battery: Battery):
        self.face = Face(lcd, battery)
        self.touch = touch
        self.gyro = gyro
        self.player = PiezoPlayer(piezo)

        self.freefall_ms = 0

        # Initial state
        lcd.set_brightness(60)
        self.player.play(SOUND_HELLO)
    
    def simulate(self, dt_ms: int):
        
        # Check gestures
        gesture = self.touch.gesture
        if gesture == Touch.UP: # Up -> feed
            self.face.set_next_face("eating", 1000)
        elif gesture == Touch.DOWN: # Down -> pet
            self.face.set_next_face("cotnent", 1000)
        
        # Check gyro
        ax, ay, az, gx, gy, gz = self.gyro.read_axyz_gxyz()
        if self.detect_drop(ax, ay, az, dt_ms): # Dropped -> dead
            self.face.set_next_face("dead", 60000, override=True)
        elif self.detect_shake(ax, ay, az, gx, gy, gz): # Shaken -> scared
            self.player.play(SOUND_EEEK)
            self.face.set_next_face("scared", 2000, override=True)
        elif self.detect_gentle(ax, ay, az, gx, gy, gz): # Gently moved -> happy
            self.face.set_next_face("happy", 2000)
    
    def detect_drop(self, ax: float, ay: float, az: float, dt_ms: int) -> bool:
        a = math.sqrt(ax*ax + ay*ay + az*az)
        if a < 0.5: # near zero-g
            self.freefall_ms += dt_ms
            if self.freefall_ms > 30: # for more than 30 ms
                self.freefall_ms = 0
                return True
        else:
            self.freefall_ms = 0
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
