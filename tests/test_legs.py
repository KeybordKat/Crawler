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

#Stand-up functions

def test_stand_is_recorded():
    """Test stand is recorded"""
    legs = MockLegs()
    legs.stand()
    assert legs.actions == ["stand"]

def test_mock_stand_fails_when_told():
    """Test mock legs fail and provide an error message when told"""
    legs = MockLegs(fail=True)
    with pytest.raises(HardwareError):
        legs.stand()

def test_failed_stand_is_not_recorded():
    """Test failed stand is not recorded"""
    legs = MockLegs(fail=True)
    with pytest.raises(HardwareError):
        legs.stand()
    assert legs.actions == []

#Sit-down functions

def test_sit_is_recorded():
    """Test sit is recorded"""
    legs = MockLegs()
    legs.sit()
    assert legs.actions == ["sit"]

def test_mock_sit_fails_when_told():
    """Test mock legs fail and provide an error message when told"""
    legs = MockLegs(fail=True)
    with pytest.raises(HardwareError):
        legs.sit()

def test_failed_sit_is_not_recorded():
    """Test failed sit is not recorded"""
    legs = MockLegs(fail=True)
    with pytest.raises(HardwareError):
        legs.sit()
    assert legs.actions == []