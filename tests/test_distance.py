#imports
from crawler.hal.distance import Distance, MockDistance
from crawler.core.errors import HardwareError
import pytest

@pytest.fixture(params=["mock"])
def sensor(request):
    """Fixture for a distance sensor"""
    return MockDistance(distance_cm=25.0)

def test_mock_returns_distance():
    """Test mock sensor returns the correct distance"""
    sensor = MockDistance(distance_cm=25.0)
    assert sensor.read() == 25.0

def test_mock_fail_when_told():
    """Test mock sensor fails and provides an error message when told"""
    sensor = MockDistance(distance_cm=25.0, fail=True)
    with pytest.raises(HardwareError):
        sensor.read()

def test_distance_cannot_be_created_directly():
    """Test Distance class cannot be created directly"""
    with pytest.raises(TypeError):
        Distance()

def test_mock_is_distance():
    """Test the mock sensor counts as Distance"""
    assert isinstance(MockDistance(distance_cm=25.0), Distance)

def test_read_returns_float(sensor):
    """Test the read method returns a float"""
    assert isinstance(sensor.read(), float)

def test_read_is_positive(sensor):
    """Test the read method returns a positive number"""
    assert sensor.read() >= 0