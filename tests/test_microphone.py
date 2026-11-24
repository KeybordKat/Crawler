#imports
import pytest
from crawler.core.errors import HardwareError
from crawler.hal.microphone import MockMicrophone, Microphone

@pytest.fixture(params=["mock"])
def microphone(request):
    """Fixture for a microphone"""
    return MockMicrophone()

def test_mock_is_microphone():
    """Test the mock microphone counts as Microphone"""
    assert isinstance(MockMicrophone(), Microphone)

def test_microphone_cannot_be_created_directly():
    """Test Microphone class cannot be created directly"""
    with pytest.raises(TypeError):
        Microphone()

def test_record_returns_bytes(microphone):
    """Test record returns bytes"""
    audio = microphone.record(1)
    assert isinstance(audio, bytes)

def test_mock_fails_when_told():
    """Test mock microphone fails when told to"""
    microphone = MockMicrophone(fail=True)
    with pytest.raises(HardwareError):
        microphone.record(1)

@pytest.mark.parametrize("seconds", ["Hi", None, 0, -1, True, 61])
def test_record_rejects_bad_requests(microphone, seconds):
    """Test record rejects bad requests"""
    with pytest.raises(ValueError):
        microphone.record(seconds)

@pytest.mark.parametrize("seconds", [1, 60, 0.5])
def test_record_accepts_good_requests(microphone, seconds):
    """Test record accepts good requests"""
    assert isinstance(microphone.record(seconds), bytes)