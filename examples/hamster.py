from abc import ABC, abstractmethod
from enum import Enum, auto
import time


class HamsterState(Enum):
    IDLE = auto()
    SLEEPING = auto()
    RUNNING = auto()
    DEAD = auto()

class Hamster(ABC):
    state: HamsterState = HamsterState.IDLE
    
    weight: float = 1.0
    energy: float = 1.0

    last_update: int

    def __init__(self, epoch_seconds: int) -> None:
        self.last_update = epoch_seconds

    def on_time(self, epoch_seconds: int):
        dth = (epoch_seconds - self.last_update) / 3600
        if dth <= 0:
            return
        
        if self.state == HamsterState.IDLE:
            self.energy -= 100 / 12 * dth # Loses energy in 12h
            self.weight -= 100 / 24 * dth # Starves in 24h
        elif self.state == HamsterState.SLEEPING:
            self.energy += 100 / 12 * dth # Recovers energy in 12h
            self.weight -= 100 / 48 * dth # Starves in 48h
        elif self.state == HamsterState.RUNNING:
            self.energy -= 100 / 6 * dth # Loses energy in 6h
            self.weight -= 100 / 12 * dth # Starves in 12h
        elif self.state == HamsterState.DEAD:
            return
        
        self.energy = max(0, min(100, self.energy))
        self.weight = max(0, min(200, self.weight))

        tm = time.localtime(epoch_seconds)
        hour = tm.tm_hour

        if self.weight == 0 or self.weight == 200:
            self.state = HamsterState.DEAD
        elif self.energy < 10 or (hour > 6 and hour < 18): # Sleeps if too tired, and daylight hours
            self.state = HamsterState.SLEEPING
        elif self.energy < 50:
            self.state = HamsterState.IDLE
        else:
            self.state = HamsterState.RUNNING

        self.last_update = epoch_seconds

    @abstractmethod
    def squeak(self):
        raise NotImplementedError

