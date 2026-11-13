#Imports
import pytest   #Main python testing library
from crawler.core.errors import HardwareError

def test_hardware_error():
    """Does the hardware error carry the correct message when raised?"""
    with pytest.raises(HardwareError) as excinfo:
        raise HardwareError("sensor timeout")
    assert str(excinfo.value) == "sensor timeout"