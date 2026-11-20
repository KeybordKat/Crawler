#imports
import pytest
from crawler.core.errors import HardwareError
from crawler.hal.legs import Legs, MockLegs

def test_legs_cannot_be_created_directly():
    """Test Legs class cannot be created directly"""
    with pytest.raises(TypeError):
        Legs()

def test_mock_is_legs():
    """Test the mock legs counts as Legs"""
    assert isinstance(MockLegs(), Legs)

def test_walk_is_recorded():
    """Test walk is recorded properly with all arguments"""
    legs = MockLegs()
    legs.walk("forward", 3, 50)
    assert legs.actions == [("walk", "forward", 3, 50)]

def test_failed_walk_is_not_recorded():
    """Test failed walk is not recorded (and fails when told)"""
    legs = MockLegs(fail=True)
    with pytest.raises(HardwareError):
        legs.walk("forward", 3, 50)
    assert legs.actions == []

#Test failed actions are not recorded and raise a hardware error
@pytest.mark.parametrize("action", ["stand", "sit"])
def test_failed_actions_are_not_recorded(action):
    """Test failed actions are not recorded"""
    legs = MockLegs(fail=True)
    with pytest.raises(HardwareError):
        getattr(legs, action)()
    assert legs.actions == []

@pytest.mark.parametrize("direction, steps, speed", [
    ("forward", 3, 101),    #Speed can't be over 100
    ("forward", 3, -1),     #Speed can't be under 0
    ("sideways", 3, 50),    #Direction must be forward or backward
    ("forward", 0, 50),     #Steps must be over 0
    ("forward", -3, 50),    #Steps must be a positive integer
    ("forward", 1.5, 50),   #Steps must be an integer
])
def test_walk_rejects_bad_request(direction, steps, speed):
    """Test walk rejects bad requests"""
    legs = MockLegs()
    with pytest.raises(ValueError):
        legs.walk(direction, steps, speed)

@pytest.mark.parametrize("action", ["stand", "sit"])
def test_action_is_recorded(action):
    """Check if actions are recorded"""
    legs = MockLegs()
    getattr(legs, action)()
    assert legs.actions == [(action,)]
