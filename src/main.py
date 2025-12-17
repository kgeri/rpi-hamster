from hamster import Hamster
from lib.waveshare import Battery_WS_RP2350, Gyro_QMI8658, LCD_GC9A01A, Piezo_WS_RP2350, Touch_CST816T
import gc
import machine
import time


TICK_MS = 10
LOW_MEM = 520 * 1024 // 10 # WS-RP2350 has 520KB SRAM, we'd want at least 10% free

def memory_watchdog():
    free = gc.mem_free()
    alloc = gc.mem_alloc()
    print("[GC] Stats: free=", free, ", alloc=", alloc, sep="")
    if free < LOW_MEM:
        print("[GC] Collect: ", sep="", end=None)
        gc.collect()
        free = gc.mem_free()
        alloc = gc.mem_alloc()
        print("free=", free, ", alloc=", alloc, sep="")
        if free < LOW_MEM:
            print("[GC] GC Failed, reset...")
            machine.reset()

t = 0
hs = Hamster(
    LCD_GC9A01A(), 
    Touch_CST816T(),
    Gyro_QMI8658(),
    Piezo_WS_RP2350(),
    Battery_WS_RP2350(),
    time.ticks_ms(),
    TICK_MS
)
while True:
    hs.tick(time.ticks_ms())
    time.sleep_ms(TICK_MS)
    
    t += 1
    if t % 1000 == 0:
        memory_watchdog()
