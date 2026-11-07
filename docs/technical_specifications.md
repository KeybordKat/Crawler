# SunFounder PiCrawler — Technical Specifications

## Mechanical

| Property | Value |
|---|---|
| Configuration | 4-legged quadruped |
| Legs / DOF | 4 legs × 3 joints = **12 DOF** |
| Joints per leg | Coxa (hip rotation), Femur (up/down), Tibia (shank) |
| Body material | Aluminum alloy chassis and brackets |
| Assembled footprint | ~280 × 165 × 51 mm |
| Body weight (no battery) | ~585 g |
| Total weight (with battery + accessories) | ~1.05 kg |

---

## Servos: SF3218MG

12 identical digital metal-gear servos, 3 per leg.

| Property | Value |
|---|---|
| Model | SunFounder SF3218MG |
| Gear train | 5-stage full metal, aluminum case, dual bearing |
| Rotation range | 270° physical; software range −90° to +90° from neutral |
| Torque @ 4.8 V | ~20.5 kg·cm |
| Torque @ 7.2 V | ~22.8 kg·cm (317 oz-in) |
| Speed @ 4.8 V | 0.18 s/60° |
| Speed @ 7.2 V | 0.14 s/60° |
| Stall current | 2.1–2.7 A per servo |
| Control signal | Digital PWM, 50 Hz, 500–2500 µs pulse, 1500 µs neutral, 5 µs dead band |
| Operating voltage | 4.8–7.2 V |
| Weight | 56 g ± 5% |
| Connector | JR universal, 320 mm wire |
| Water resistance | Splash-resistant |

### Servo-to-Leg Mapping (PWM channels)

```python
PIN_LIST = [9, 10, 11,   # Leg 1: Right Front  (Coxa, Femur, Tibia)
             3,  4,  5,   # Leg 2: Left Front
             0,  1,  2,   # Leg 3: Left Rear
             6,  7,  8]   # Leg 4: Right Rear
```

---

## Controller: Robot HAT V4

Raspberry Pi HAT providing servo control, ADC, digital I/O, audio, and power management.

| Property | Value |
|---|---|
| MCU | Artery AT32F413CBT7 (ARM Cortex-M4, 150 MHz, 256 KB Flash, 32 KB SRAM) |
| I2C address | **0x14** (7-bit) |
| PWM channels | 12 servo (P0–P11) + 2 motor (PWM12/13) |
| PWM frequency | 50 Hz |
| ADC channels | A0–A3 (12-bit, 0–3.3 V) + A4 for battery voltage |
| Digital I/O | D0=GPIO17, D1=GPIO4, D2=GPIO27, D3=GPIO22 |
| I2C (standard) | P2.54 4-pin; GPIO2/3; 10 kΩ pull-ups |
| I2C (QWIIC) | SH1.0 4-pin (QWIIC / STEMMA QT compatible) |
| SPI | P2.54 7-pin; GPIO 6/8/9/10/11 |
| UART | P2.54 4-pin |
| Motor driver | 2 channels; Motor1: GPIO23 dir + PWM13; Motor2: GPIO24 dir + PWM12 |
| Audio out | I2S mono speaker, 8 Ω 1 W (GPIO18/19/21) |
| Microphone | None on V4 (V5 adds onboard I2S MEMS mic) |
| User controls | 1 LED (GPIO26), USR button (GPIO25), RST button (GPIO16) |
| Power input | 6.0–8.4 V via XH2.54 3-pin |
| Charging port | Type-C USB 5 V/2 A (~10 W), integrated balancer |

### Expansion Headers Summary

| Header | Connector | Signals | Notes |
|---|---|---|---|
| PWM P0–P11 | P2.54 3-pin | +5V, GND, PWM | All 12 used by servos |
| Digital D0–D3 | P2.54 3-pin | +3.3V, GND, GPIO | D2+D3 used by ultrasonic |
| ADC A0–A3 | P2.54 3-pin | +3.3V, GND, analog | 12-bit, 0–3.3 V |
| I2C (QWIIC) | SH1.0 4-pin | +3.3V, GND, SDA, SCL | Shares bus at 0x14 |
| SPI | P2.54 7-pin | +3.3V, GND, CS, SCK, MOSI, MISO, BSY | |
| UART | P2.54 4-pin | +3.3V, GND, TX, RX | |
| Motor ports | XH2.54 2-pin | Motor+, Motor− | 5 V / 1.8 A each |

### I2C Address Map

| Device | Address |
|---|---|
| Robot HAT MCU (all PWM/ADC) | 0x14 |
| VL53L0X ToF (optional) | 0x29 |
| ICM-20948 IMU (optional) | 0x68 or 0x69 |

---

## Power System

| Property | Value |
|---|---|
| Chemistry | Li-ion, 2 × 18650 in 2S series |
| Nominal voltage | 7.4 V |
| Full charge | 8.4 V |
| Over-discharge cutoff | 6.0 V |
| Capacity | 2000 mAh / 14.8 Wh |
| Connector | XH2.54 3-pin |
| Weight | 90.8 g |
| Runtime | ~90 min at moderate load (estimated) |

---

## Included Sensors

### Camera: OV5647

| Property | Value |
|---|---|
| Resolution | 5 MP (2592 × 1944 still) |
| Video modes | 1080p30, 720p60, 640×480p90 |
| FOV | 65° |
| Aperture | F1.8 |
| Interface | CSI ribbon to Raspberry Pi |
| Dimensions | 24 × 23.5 × 8 mm |
| Weight | 3 g |

### Ultrasonic: HC-SR04

| Property | Value |
|---|---|
| Range | 2–500 cm |
| Accuracy | ±3 mm |
| Interface | GPIO digital (TRIG → D2/GPIO27, ECHO → D3/GPIO22) |

---

## Raspberry Pi Compatibility

| RPi Model | Python SDK | EzBlock |
|---|---|---|
| RPi 5 | Yes | No |
| RPi 4B | Yes | Yes |
| RPi 3B+ / 3B | Yes | Yes |
| RPi Zero 2W | Yes | Yes |

Raspberry Pi is **not included** in any kit variant.

---

## Kit Contents

- Aluminum chassis parts (pre-assembled)
- 12 × SF3218MG servos
- Robot HAT V4
- OV5647 5 MP CSI camera module
- HC-SR04 ultrasonic module
- 7.4 V 2000 mAh 18650 battery pack
- USB-C charging cable
- Calibration chart (printed)
- Assembly instructions
- All mounting hardware
