# SunFounder PiCrawler — Software Reference

## Stack Overview

```
picrawler          # core robot library (GPL-3.0)
  └── robot-hat    # HAT driver: PWM, ADC, GPIO, I2S, Servo, Music
vilib              # vision: camera, detection, web streaming
```

GitHub repos:
- https://github.com/sunfounder/picrawler
- https://github.com/sunfounder/robot-hat
- https://github.com/sunfounder/vilib

---

## Installation (Raspberry Pi)

```bash
sudo apt install git python3-pip python3-setuptools python3-smbus

git clone -b 2.5.x --depth=1 https://github.com/sunfounder/robot-hat.git
cd robot-hat && sudo python3 install.py

cd ~/ && git clone --depth=1 https://github.com/sunfounder/vilib.git
cd vilib && sudo python3 install.py

git clone https://github.com/sunfounder/picrawler.git
sudo pip3 install ~/picrawler --break-system-packages
```

---

## `Picrawler` Class

Extends `Robot` from `robot-hat`. Offset config stored at `~/.config/.picrawler.config`.

### Constants

```python
class Picrawler(Robot):
    A = 48      # Coxa link length (mm)
    B = 78      # Femur link length (mm)
    C = 33      # Tibia offset (mm)
    PIN_LIST = [9, 10, 11, 3, 4, 5, 0, 1, 2, 6, 7, 8]
```

### Constructor

```python
Picrawler(pin_list=PIN_LIST, init_angles=None)
```

### Leg Coordinate System

Origin = body-side servo hub for each leg.
- X: lateral (outward positive)
- Y: fore-aft
- Z: vertical (negative = down toward ground)
- Default standing position: `[60, 0, -30]` mm

### Kinematics

```python
coord2polar(coord)       # [x, y, z] → joint angles list
polar2coord(angles)      # joint angles → [x, y, z]
limit_angle(angles)      # clamp to mechanical limits
```

### Motion Execution

```python
do_action(motion_name, step=1, speed=50)
# Run a named gait N steps. speed = 1–100.

do_step(step, speed=50, israise=False)
# Execute one motion frame directly.

set_angle(angles_list, speed=50, israise=False)
# Set all 12 servo angles.

servo_move(translate_list, speed)
# Low-level hardware move.
```

### State Queries

```python
current_step_all_leg_angle()      # → 12-element angle list
current_step_all_leg_value()      # → all leg [x,y,z] coordinates
current_step_leg_value(leg)       # → [x,y,z] for leg 1–4
```

### Body / Single-Leg Control

```python
do_single_leg(leg, coordinate, speed)         # isolate one leg
mix_step(basic_step, leg, coordinate)         # blend custom + gait frame
rotate_body_absolute_x(degree_x)             # pitch
rotate_body_absolute_y(degree_y)             # yaw (body, not heading)
move_body_absolute(x, y, z)                  # body translation
```

### Calibration

```python
cali_helper_web(leg, pos, enter)             # interactive web-based offset tool
add_action(action_name, action_list)         # register custom motion sequence
```

---

## Built-in Gaits (`MoveList`)

| Name | Description |
|---|---|
| `forward` | Walk forward |
| `backward` | Walk backward |
| `turn_left` | Rotate left in place |
| `turn_right` | Rotate right in place |
| `turn_left_angle` | Angled left turn |
| `turn_right_angle` | Angled right turn |
| `stand` | Stand up from rest |
| `sit` | Lower to rest posture |
| `ready` | Preparation stance |
| `wave` | Front leg wave gesture |
| `look_left` / `look_right` | Body pan left/right |
| `look_up` / `look_down` | Body tilt up/down |
| `push_up` | Push-up exercise motion |
| `dance` | Choreographed circular motion |

Usage:

```python
from picrawler import Picrawler
crawler = Picrawler()
crawler.do_action("forward", step=3, speed=80)
```

---

## Ultrasonic Sensor

```python
from robot_hat import Ultrasonic, Pin

sonar = Ultrasonic(Pin("D2"), Pin("D3"))  # TRIG, ECHO
distance = sonar.read()                    # float in cm (median of 5 samples)
```

---

## `Servo` Class (robot-hat)

```python
from robot_hat import Servo

s = Servo("P0")          # pin name P0–P11
s.angle(45)              # degrees: -90 to +90; 0 = center
s.pulse_width_time(1500) # microseconds: 500–2500
```

---

## `Music` Class (robot-hat)

```python
from robot_hat import Music

music = Music()
music.sound_play("/path/to/file.wav")
music.sound_play_threading("/path/to/file.wav")
music.music_play("/path/to/file.mp3")
music.music_stop()
music.music_pause()
music.music_resume()
music.play_tone_for(frequency_hz, duration_s)
# Volume: music.set_volume(0–100)
```

---

## Vision: `vilib`

Camera streams MJPEG to `http://<ip>:9000/mjpg`. Frame size: 320 × 240.

```python
from vilib import Vilib

Vilib.camera_start(vflip=False, hflip=False)
Vilib.display(local=True, web=True)
Vilib.camera_close()
Vilib.take_photo(name, path)

# Detection toggles
Vilib.face_detect_switch(True)
Vilib.color_detect("red")           # red/orange/yellow/green/blue/purple
Vilib.color_detect_switch(True)
Vilib.qrcode_detect_switch(True)
Vilib.gesture_detect_switch(True)
Vilib.traffic_sign_detect_switch(True)
```

### Detection Results

All results in `Vilib.detect_obj_parameter` dict:

```python
# Color detection
Vilib.detect_obj_parameter["color_x"]   # center x
Vilib.detect_obj_parameter["color_y"]   # center y
Vilib.detect_obj_parameter["color_w"]   # bounding box width
Vilib.detect_obj_parameter["color_h"]   # bounding box height
Vilib.detect_obj_parameter["color_n"]   # object count

# Face detection
Vilib.detect_obj_parameter["human_x"]
Vilib.detect_obj_parameter["human_y"]
Vilib.detect_obj_parameter["human_n"]

# QR code
Vilib.detect_obj_parameter["qr_data"]   # decoded string
Vilib.detect_obj_parameter["qr_x"]
Vilib.detect_obj_parameter["qr_y"]

# Gesture: "paper", "scissor", "rock"
Vilib.detect_obj_parameter["gesture_t"]

# Traffic sign: "stop", "right", "left", "forward"
Vilib.detect_obj_parameter["traffic_sign_t"]
```

---

## AI / Voice Stack (OpenClaw)

### Ollama (local LLM)

```python
from picrawler.llm import Ollama

llm = Ollama(model="llama3.2:3b", base_url="http://localhost:11434")
response = llm.chat([{"role": "user", "content": "Walk forward 3 steps"}])
```

Supports: llama3.2:3b, qwen2.5:7b, mistral, and any OpenAI-compatible endpoint (GPT-4o, Gemini, Grok, DeepSeek, Qwen).

### VoiceActiveCrawler

```python
from picrawler.voice_assistant import VoiceActiveCrawler

bot = VoiceActiveCrawler(
    stt_language="en",
    tts_model="en_US-ryan-low",
    llm_model="llama3.2:3b",
)
bot.run()
# Pipeline: wake word → STT → LLM → TTS → robot action
```

---

## Calibration Workflow

1. Place robot on the printed calibration chart (included in kit).
2. Run:
   ```bash
   sudo python3 ~/picrawler/examples/calibration/calibration.py
   ```
3. Keys 2/3 select left legs; 1/4 select right legs; WASD/RF adjust position.
4. Spacebar saves offsets to `~/.config/.picrawler.config`.
5. Confirm with `Y`.

---

## Communication Modes

| Mode | Description |
|---|---|
| WiFi AP | RPi creates hotspot `SunFounder_XXXX`; EzBlock app connects |
| WiFi STA | RPi joins existing network; connect by IP |
| SSH | Standard over any network |
| VNC | Remote desktop |
| Web video | `Vilib.display(web=True)` → `http://<ip>:9000/mjpg` |
| EzBlock Studio | Official graphical IDE (iOS/Android/Web); no RPi 5 support |

---

## Package Structure

```
picrawler/
  picrawler.py          # Picrawler class + MoveList
  llm.py                # Ollama wrapper (OpenAI-compatible)
  stt.py                # Speech-to-Text
  tts.py                # Text-to-Speech
  voice_assistant.py    # VoiceActiveCrawler orchestrator
  version.py
```
