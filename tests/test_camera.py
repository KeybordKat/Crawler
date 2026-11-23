#imports
from crawler.hal.camera import MockCamera, Camera
from crawler.core.errors import HardwareError
import pytest

@pytest.fixture(params=['mock'])
def camera(request):
    """Fixture for a camera"""
    return MockCamera()

def test_mock_is_camera():
    """Test the mock camera counts as Camera"""
    assert isinstance(MockCamera(), Camera)

def test_take_photo_returns_bytes(camera):
    """Test take photo returns bytes"""
    photo = camera.take_photo()
    assert isinstance(photo, bytes)

def test_mock_fails_when_told():
    """Test mock camera fails when told to"""
    camera = MockCamera(fail=True)
    with pytest.raises(HardwareError):
        camera.take_photo()