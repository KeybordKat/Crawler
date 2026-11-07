# PiCrawler Setup Progress

## Hardware
- [x] Robot fully assembled
- [x] Raspberry Pi 3B+ selected
- [x] 64-bit Raspberry Pi OS Lite flashed to SD card
- [x] Robot HAT V4 seated on GPIO header
- [x] 12 servo cables connected to PWM channels P0–P11
- [x] Ultrasonic sensor connected (TRIG → D2, ECHO → D3)
- [x] Camera connected via CSI ribbon cable
- [x] Battery pack connected to HAT power input

## Raspberry Pi Setup
- [x] First boot — Pi joined WiFi, reachable at `picrawler.local`
- [x] OS updated (`apt update && full-upgrade`)
- [x] Locale fixed (`en_US.UTF-8`)
- [x] Camera interface enabled
- [x] `git`, `python3-pip`, `python3-setuptools`, `python3-smbus` installed
- [x] `robot-hat` (2.5.x) cloned and installed (`~/robot-hat`)
- [x] `vilib` cloned and installed (`~/vilib`)
- [x] `picrawler` cloned and installed (`~/picrawler`)
- [x] Robot HAT detected on I2C bus at `0x14`
- [x] Servo calibration complete (`~/picrawler/examples/0_calibration.py`)
- [x] First movement test passed — robot stood and walked forward

## Setup Complete

The robot is fully operational. Next steps are up to you — see `expansion_ideas.md` for ideas.