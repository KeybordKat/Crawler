#imports
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

    @abstractmethod
    def turn(self, direction, steps, speed):
        """Turn based on given variables"""
        pass

    def _check_request(self, directions, direction, steps, speed):
        """helper method to check general rules for leg movements"""
        if speed < 0 or speed > 100:
            raise ValueError("speed must be between 0 and 100")
        #Check direction provided is within provided list of allowed directions
        if direction not in directions:
            raise ValueError("direction must be " + " or ".join(directions))
        if not isinstance(steps, int):
            raise ValueError("steps must be an integer")
        if steps < 1:
            raise ValueError("steps must be at least 1")


class MockLegs(Legs):
    """Mock legs for testing"""
    def __init__(self, fail=False):
        self.actions = []
        self.fail = fail

    def stand(self):
        if self.fail:
            raise HardwareError("legs failed to stand")
        self.actions.append(("stand",))

    def sit(self):
        if self.fail:
            raise HardwareError("legs failed to sit")
        self.actions.append(("sit",))

    def walk(self, direction, steps, speed):
        #check all provided parameters are valid
        self._check_request(("forward", "backward"), direction, steps, speed)
        #legs fail when told (last so we know all other actions were successful)
        if self.fail:
            raise HardwareError("legs failed to walk")
        self.actions.append(("walk", direction, steps, speed))

    def turn(self, direction, steps, speed):
        #Check all provided parameters are valid
        self._check_request(("left", "right"), direction, steps, speed)
        #turn fails when told (last so we know all other actions were successful)
        if self.fail:
            raise HardwareError("legs failed to turn")
        self.actions.append(("turn", direction, steps, speed))