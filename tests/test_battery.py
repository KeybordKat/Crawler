#imports
import pytest
from crawler.core.errors import HardwareError
from crawler.hal.battery import Battery, MockBattery

@pytest.fixture(params=["mock"])
def battery(request):
    """Fixture for a battery sensor"""
    return MockBattery(voltage=7.4)

def test_mock_returns_voltage():
    """Test mock battery returns the correct voltage"""
    battery = MockBattery(voltage=7.4)
    assert battery.read_voltage() == 7.4

def test_battery_cannot_be_created_directly():
    """Test Battery class cannot be created directly"""
    with pytest.raises(TypeError):
        Battery()

def test_mock_is_battery():
    """Test the mock battery counts as Battery"""
    assert isinstance(MockBattery(voltage=7.4), Battery)

def test_mock_fails_when_told():
    """Test mock battery fails and provides an error message when told"""
    battery = MockBattery(voltage=7.4, fail=True)
    with pytest.raises(HardwareError):
        battery.read_voltage()

def test_read_returns_float(battery):
    """Test the read method returns a float"""
    assert isinstance(battery.read_voltage(), float)

def test_read_is_not_negative(battery):
    """Test the read method doesn't return negatives"""
    assert battery.read_voltage() >= 0