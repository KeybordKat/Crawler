#imports
from crawler.hal.assembler import assemble_hal
from crawler.hal.speaker import MockSpeaker
from crawler.hal.camera import MockCamera
from crawler.hal.legs import MockLegs
from crawler.hal.battery import MockBattery
from crawler.hal.distance import MockDistance
import pytest

@pytest.mark.parametrize("name, mock_class", [
    ("speaker", MockSpeaker),
    ("camera", MockCamera),
    ("legs", MockLegs),
    ("battery", MockBattery),
    ("distance", MockDistance),
])
def test_mock_hal_has_mock_devices(name, mock_class):
    """Check if mock hal correctly selects mock device types"""
    hal = assemble_hal(real=False)
    assert isinstance(getattr(hal, name), mock_class)