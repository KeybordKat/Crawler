from crawler.hal.speaker import MockSpeaker
from crawler.hal.camera import MockCamera
from crawler.hal.legs import MockLegs
from crawler.hal.battery import MockBattery
from crawler.hal.distance import MockDistance
from crawler.hal.microphone import MockMicrophone

class Hal:
    def __init__(self, speaker, camera, legs, battery, distance, microphone):
        self.speaker = speaker
        self.camera = camera
        self.legs = legs
        self.battery = battery
        self.distance = distance
        self.microphone = microphone

def assemble_hal(real=False):
    """Assemble hal"""
    return Hal(
        speaker=MockSpeaker(),
        camera=MockCamera(),
        legs=MockLegs(),
        battery=MockBattery(voltage=7.4),
        distance=MockDistance(distance_cm=10),
        microphone=MockMicrophone()
    )