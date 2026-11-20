from abc import ABC, abstractmethod
from crawler.core.errors import HardwareError

class Legs(ABC):
    """Abstract base class for legs"""
    @abstractmethod
    def stand(self):
        """Stand up"""
        pass

    @abstractmethod
    def sit(self):
        """Sit down"""
        pass

    @abstractmethod
    def walk(self, direction, steps, speed):
        """Walk a given distance"""
        pass

class MockLegs(Legs):
    """Mock legs for testing"""
    def __init__(self, fail=False):
        self.actions = []
        self.fail = fail

    def stand(self):
        if self.fail:
            raise HardwareError("legs failed")
        self.actions.append(("stand",))

    def sit(self):
        if self.fail:
            raise HardwareError("legs failed")
        self.actions.append(("sit",))

    def walk(self, direction, steps, speed):
        #only accept valid speed
        if speed < 0 or speed > 100:
            raise ValueError("speed must be between 0 and 100")
        #only accept valid direction
        if direction not in ("forward", "backward"):
            raise ValueError("direction must be forward or backward")
        #Only accept integer steps
        if not isinstance(steps, int):
            raise ValueError("steps must be an integer")
        #only accept valid number of steps
        if steps < 1:
            raise ValueError("steps must be at least 1")
        #legs fail when told (last so we know all other actions were successful)
        if self.fail:
            raise HardwareError("legs failed")
        self.actions.append(("walk", direction, steps, speed))