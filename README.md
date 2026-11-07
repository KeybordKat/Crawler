# PiCrawler Project

Development workspace for the **SunFounder PiCrawler** — a 12-DOF quadruped robot built on Raspberry Pi.

## Documentation

- [`docs/technical_specifications.md`](docs/technical_specifications.md) — Hardware specs, servo data, controller board, sensors, power system
- [`docs/software_reference.md`](docs/software_reference.md) — Python SDK, core classes, gait API, vision, AI stack
- [`docs/expansion_ideas.md`](docs/expansion_ideas.md) — Ideas for hardware and software extensions

## Project Layout

| Path | Purpose |
|---|---|
| `src/` | Your own code. Written here, uploaded to the Pi for testing |
| `vendor/` | Read-only git submodules of SunFounder's `picrawler`, `robot-hat`, `vilib` (reference only; already installed on the Pi; never edit or upload) |
| `docs/` | Specs, SDK reference, expansion ideas, setup log |

After cloning, run `git submodule update --init` to fetch `vendor/`.

## Quick Links

| Resource | URL |
|---|---|
| Official docs | https://docs.sunfounder.com/projects/pi-crawler/en/latest/ |
| picrawler GitHub | https://github.com/sunfounder/picrawler |
| robot-hat GitHub | https://github.com/sunfounder/robot-hat |
| vilib GitHub | https://github.com/sunfounder/vilib |
| Robot HAT V4 docs | https://docs.sunfounder.com/projects/robot-hat-v4/en/latest/ |

## Setup

```bash
# On the Raspberry Pi:
sudo apt install git python3-pip python3-setuptools python3-smbus

git clone -b 2.5.x --depth=1 https://github.com/sunfounder/robot-hat.git
cd robot-hat && sudo python3 install.py

cd ~/ && git clone --depth=1 https://github.com/sunfounder/vilib.git
cd vilib && sudo python3 install.py

git clone https://github.com/sunfounder/picrawler.git
sudo pip3 install ~/picrawler --break-system-packages
```
