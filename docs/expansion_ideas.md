# SunFounder PiCrawler — Expansion Ideas

## Hardware Expansions

### Sensors

| Sensor | Interface | Benefit | Notes |
|---|---|---|---|
| **IMU (ICM-20948)** | I2C QWIIC (0x68/0x69) | Body tilt sensing, terrain adaptation, fall detection | Adafruit breakout confirmed working via STEMMA QT |
| **ToF distance (VL53L0X)** | I2C QWIIC (0x29) | Precise short-range obstacle detection (1 mm resolution) | Confirmed working via STEMMA QT; complements HC-SR04 |
| **LiDAR (RPLidar A1)** | UART | 360° 2D mapping, SLAM, autonomous navigation | Mounts overhead; heavier; requires motor power |
| **IR line follower** | I2C QWIIC | Line-following behavior | SunFounder 5-ch TCRT5000 module electrically compatible |
| **Soil/moisture sensors** | ADC A0–A3 | Environmental sensing applications | 3.3 V-safe; direct to ADC headers |
| **Gas / air quality (SGP30)** | I2C QWIIC | Environmental monitoring | Low power; useful for indoor inspection use case |
| **Pressure / BMP280** | I2C QWIIC | Altitude and environmental data | |

### Compute Upgrades

| Upgrade | Benefit | Trade-offs |
|---|---|---|
| **RPi 5 (8 GB or 16 GB)** | Faster inference, more RAM for CV | EzBlock not supported; runs warmer |
| **Hailo-8L AI HAT** | Hardware neural network acceleration (26 TOPS) | Expensive (~$70); RPi 5 only; enables real-time detection without GPU |
| **Coral USB Accelerator** | 4 TOPS edge TPU; model inference at ~400 FPS | USB 3.0 speeds only on RPi 4+ |
| **Pi Zero 2W (secondary)** | Dedicated sensor node (IMU/gyro), offloads main RPi | Communicates over I2C or USB serial; small form factor |

### Actuators & Effectors

| Addition | Description |
|---|---|
| **Gripper / claw** | Servo-driven end-effector on front leg; enables pick-and-place; replace one front tibia servo |
| **Tail / counterbalance** | Servo-driven rear appendage to shift CoM during climbing |
| **Active LED eyes** | I2C OLED displays (SSD1306 or SSD1351) for expression/emotion display — popular community mod |
| **Louder speaker** | Replace onboard 1 W with external 3–5 W for voice assistant clarity |
| **Stronger servos** | Upgrade tibias to higher-torque servos (e.g., SF3220) to improve load capacity on rough terrain |

### Power

| Upgrade | Benefit |
|---|---|
| **Higher-capacity 18650 pack (3000–3500 mAh)** | Extends runtime from ~90 min to ~2+ hrs |
| **Independent servo power rail** | Bypass the HAT power path; use a separate regulator for servos to protect RPi from voltage sag under heavy load |
| **PoE HAT** | Power over Ethernet for tethered indoor operations (no battery concern) |
| **Solar panel** | Trickle-charge via USB-C input for extended outdoor missions |

---

## Software Expansions

### Navigation & Autonomy

- **SLAM with LiDAR + ROS2**: Map an environment and navigate autonomously.
  The community project [SpiritualCreations42/PicrawlerV2](https://github.com/SpiritualCreations42/PicrawlerV2) is building Ubuntu 24.04 + ROS2 + Gazebo URDF simulation on RPi 5.

- **Visual odometry**: Use camera frames + optical flow to estimate displacement without wheel encoders.

- **Obstacle field navigation**: Combine HC-SR04 (long range) + VL53L0X (precise near-field) for layered avoidance with head-turn scanning.

- **IMU-based terrain adaptation**: Read roll/pitch from ICM-20948 and dynamically adjust body height and leg extension to maintain level gait on slopes.

### Computer Vision

- **Person following**: Track a detected face/body centroid and steer toward it using `Vilib.detect_obj_parameter["human_x"]` as an error signal.

- **Color-target hunting**: Navigate toward a specific detected color; useful for fetch or herding demos.

- **QR code missions**: Scan QR codes to receive waypoints or commands without network connectivity.

- **Custom classifier (TFLite / ONNX)**: Deploy a custom-trained object detector via Hailo-8L or Coral USB; replace `vilib` traffic sign detector with a domain-specific model.

### Gait Research

- **CPG (Central Pattern Generator)**: Implement oscillator-based gait generation instead of fixed motion lists; enables smooth speed transitions and adaptive timing.

- **Reinforcement learning gait**: Train gaits in simulation (Isaac Gym / Gazebo) and deploy onto the real robot via sim-to-real transfer.

- **Terrain-aware gait switching**: Detect surface type (smooth / rough / incline) from IMU + camera and automatically switch gait (walk / trot / crawl).

- **Foot contact detection**: Add force-sensitive resistors (FSR) under each foot tip; detect ground contact timing to close the gait loop.

### AI / Voice

- **Wake-word customization**: Train a custom wake word with Porcupine or openWakeWord to replace the default.

- **Tool-use LLM agent**: Give the LLM tools (move, look, take_photo, speak) and let it plan multi-step behaviors from natural language commands.

- **Emotion state machine**: Map LLM sentiment analysis of conversation to LED eye expressions and body posture.

- **Cloud fallback / local primary**: Route inference to local Ollama normally; fall back to GPT-4o when local model confidence is low.

### Remote Control & Monitoring

- **WebSocket gamepad control**: Build a browser UI with a virtual gamepad (or connect a physical USB gamepad) for real-time teleoperation over WiFi.

- **Telemetry dashboard**: Stream battery voltage (ADC A4), servo load estimates, IMU data, and camera feed to a Grafana/InfluxDB dashboard.

- **Waypoint mission planner**: Web UI to drop waypoints on a map; robot executes the route autonomously.

- **Multi-robot coordination**: Two PiCrawlers with shared Ollama context perform collaborative tasks (one scouts, one retrieves).

---

## Community Projects to Study

| Project | What to learn |
|---|---|
| [captredbeard's Enhanced PiCrawler](https://forum.sunfounder.com/t/picrawler-upgrades/3750) | Full hardware upgrade path (Hailo-8L, OLED eyes, independent servo power, secondary Pi Zero for IMU) |
| [SpiritualCreations42/PicrawlerV2](https://github.com/SpiritualCreations42/PicrawlerV2) | Ubuntu 24.04 on RPi 5, ROS2 integration, URDF model |
| [SpiritualCreations42/PiCrawler-Upgrades](https://github.com/SpiritualCreations42/PiCrawler-Upgrades) | Web UI, sensor wiring, power distribution |

---

## Recommended First Expansions

For someone starting fresh, highest value-to-effort:

1. **IMU (ICM-20948 via QWIIC)** — unlocks terrain adaptation and fall detection with minimal wiring; plug-and-play.
2. **Custom gait via `add_action()`** — no hardware needed; explore the kinematics API and design a faster trot or a low-creep gait.
3. **Person-following behavior** — integrates vilib face detection + `turn_left`/`turn_right` gait; impressive result with ~30 lines of code.
4. **LLM voice assistant** — install Ollama (llama3.2:3b works on RPi 4 at ~1 token/s); add a USB mic; use `VoiceActiveCrawler` as a base.
5. **VL53L0X ToF sensor** — QWIIC plug-in; precise stair-edge and cliff detection.
