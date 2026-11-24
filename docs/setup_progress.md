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

## Setup Complete (on the Pi 3B+)

The robot was fully operational on the Pi 3B+. Next steps are up to you — see `expansion_ideas.md` for ideas.

## Upgrade to Raspberry Pi 5 (8 GB)
- [x] Pi 5 received and installed in the robot
- [x] Cooling fan attached
- [ ] Try the old Pi 3B+ SD card in the Pi 5. It only boots if the OS is Bookworm or newer (64-bit). If it does not boot, reflash 64-bit Raspberry Pi OS (Bookworm) Lite with Raspberry Pi Imager and set WiFi, SSH and the hostname `picrawler` there
- [ ] OS flashed to SD card (only if the old card does not boot)
- [ ] First boot, WiFi, SSH
- [ ] OS updated, locale fixed
- [ ] `robot-hat`, `vilib`, `picrawler` installed (check they work on the Pi 5)
- [ ] Robot HAT detected on I2C bus at `0x14`
- [ ] Servo calibration checked (values are stored on the card, so they may carry over if the old card is reused)
- [ ] First movement test
- [ ] Camera cable received (the old 15-pin cable does not fit the Pi 5's 22-pin CSI port) and plugged in
- [ ] Camera detected (`rpicam-hello --list-cameras`). Check `vilib` works with the Pi 5 camera stack
- [ ] Mac to Pi upload workflow set up

## New Hardware (Pi 5)
Details in `hardware_plan.md`. The robot HAT's onboard speaker was removed (it did not fit with the fan and never worked well).
- [x] Speaker chosen and bought: Pi Hut Mini External USB Stereo Speaker
- [x] Microphone chosen and bought: Pi Hut Mini USB Microphone
- [ ] Speaker and microphone received and plugged into USB
- [ ] Check both show up as audio devices on the Pi 5 (and install PulseAudio if needed)
- [ ] Set microphone input gain and test recording
- [x] Screen chosen and ordered: iPistBit 4.3" DSI IPS touch screen, 800x480
- [ ] Screen received. Check it comes with a 22-pin cable (the Pi 5 port is 22-pin)
- [ ] Screen connected and tested on the Pi 5 (fits on the robot, does not block the camera cable)