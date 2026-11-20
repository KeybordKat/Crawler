#imports
from crawler.hal.speaker import MockSpeaker, Speaker
import pytest
from crawler.core.errors import HardwareError

@pytest.fixture(params=["mock"])
def speaker(request):
    """Fixture for a speaker"""
    return MockSpeaker()

def test_mock_is_speaker():
    """test the mock speaker counts as Speaker"""
    assert isinstance(MockSpeaker(), Speaker)

def test_speak_succeeds(speaker):
    """test speak succeeds"""
    speaker.speak("hello")

def test_speaker_cannot_be_created_directly():
    """test Speaker class cannot be created directly"""
    with pytest.raises(TypeError):
        Speaker()

def test_mock_records_spoken_text():
    """test the mock speaker records spoken text"""
    speaker = MockSpeaker()
    speaker.speak("hello")
    assert speaker.spoken == ["hello"]

def test_mock_fails_when_told():
    """test the mock speaker fails when told to"""
    speaker = MockSpeaker(fail=True)
    with pytest.raises(HardwareError):
        speaker.speak("hello")

def test_failed_speak_is_not_recorded():
    """test failed speak actions aren't recorded"""
    speaker = MockSpeaker(fail=True)
    with pytest.raises(HardwareError):
        speaker.speak("hello")
    assert speaker.spoken == []

@pytest.mark.parametrize("text", [123, "", " ", None])
def test_speak_rejects_bad_requests(speaker, text):
    """test speak rejects bad requests"""
    with pytest.raises(ValueError):
        speaker.speak(text)