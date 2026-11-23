#imports
import pytest
from crawler.core.errors import HardwareError
from crawler.hal.legs import Legs, MockLegs

@pytest.fixture(params=["mock"])
def legs(request):
    """Mock Legs class"""
    return MockLegs()

#General leg tests
def test_legs_cannot_be_created_directly():
    """Test Legs class cannot be created directly"""
    with pytest.raises(TypeError):
        Legs()

def test_mock_is_legs():
    """Test the mock legs counts as Legs"""
    assert isinstance(MockLegs(), Legs)

#Walk tests
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

@pytest.mark.parametrize("direction, steps, speed", [
    ("forward", 3, 101),    #Speed can't be over 100
    ("forward", 3, -1),     #Speed can't be under 0
    ("sideways", 3, 50),    #Direction must be forward or backward
    ("forward", 0, 50),     #Steps must be over 0
    ("forward", -3, 50),    #Steps must be a positive integer
    ("forward", 1.5, 50),   #Steps must be an integer
])
def test_walk_rejects_bad_request(legs,direction, steps, speed):
    """Test walk rejects bad requests"""
    with pytest.raises(ValueError):
        legs.walk(direction, steps, speed)

@pytest.mark.parametrize("direction, steps, speed", [
    ("forward", 1, 50),
    ("backward", 1, 50),
    ("forward", 1, 0),
    ("forward", 1, 100)
])
def test_walk_succeeds(legs, direction, steps, speed):
    """Check if walk action succeeds"""
    legs.walk(direction, steps, speed)

#Sit and stand tests
@pytest.mark.parametrize("action", ["stand", "sit"])
def test_failed_actions_are_not_recorded(action):
    """Test failed actions are not recorded and raise a hardware error"""
    legs = MockLegs(fail=True)
    with pytest.raises(HardwareError):
        getattr(legs, action)()
    assert legs.actions == []

@pytest.mark.parametrize("action", ["stand", "sit"])
def test_action_is_recorded(action):
    """Check if actions are recorded"""
    legs = MockLegs()
    getattr(legs, action)()
    assert legs.actions == [(action,)]

@pytest.mark.parametrize("action", ["stand", "sit"])
def test_action_succeeds(legs, action):
    """Check if valid actions succeed"""
    getattr(legs, action)()

#Turn tests
def test_turn_is_recorded():
    """Test turn is recorded properly with all arguments"""
    legs = MockLegs()
    legs.turn("left", 2, 50)
    assert legs.actions == [("turn", "left", 2, 50)]

def test_failed_turn_is_not_recorded():
    """Test failed turn is not recorded and raises a hardware error (and fails when told)"""
    legs = MockLegs(fail=True)
    with pytest.raises(HardwareError):
        legs.turn("left", 2, 50)
    assert legs.actions == []

@pytest.mark.parametrize("speed", [101, -1])
def test_turn_rejects_bad_speed(legs, speed):
    with pytest.raises(ValueError):
        legs.turn("left", 2, speed)

@pytest.mark.parametrize("direction", ["forward", "sideways", "", "LEFT"])
def test_turn_rejects_bad_direction(legs, direction):
    with pytest.raises(ValueError):
        legs.turn(direction, 2, 50)

@pytest.mark.parametrize("steps", [0, -3, 1.5])
def test_turn_rejects_bad_steps(legs, steps):
    with pytest.raises(ValueError):
        legs.turn("left", steps, 50)

@pytest.mark.parametrize("direction, steps, speed", [
    ("left", 1, 50),
    ("right", 1, 50),
    #Edge cases
    ("left", 1, 0),
    ("left", 1, 100),
])
def test_turn_succeeds(legs, direction, steps, speed):
    """Check if valid turns succeed"""