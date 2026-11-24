# Hardware Plan: Speaker, Microphone, Display

Decided 2026-11-20. The robot HAT's onboard speaker was removed (the fan would not fit with it, and it never worked well). The Robot HAT V4 has no microphone. The Pi 5 has no 3.5mm audio jack. So audio in and out both go over USB.

Constraints: parts must ship to the UK, most parts should cost about £10 or less (the screen can cost a little more), and the screen does not need touch.

## Status

| Part | Status | Choice | Listed price |
|---|---|---|---|
| Speaker | Bought | [Pi Hut Mini External USB Stereo Speaker](https://thepihut.com/products/mini-external-usb-stereo-speaker) | £10.90 |
| Microphone | Bought | [Pi Hut Mini USB Microphone](https://thepihut.com/products/mini-usb-microphone) | £5.20 (one page showed £10.90) |
| Camera cable | Ordered, waiting | 22-pin (Pi 5 end) to 15-pin (camera end) | The old 15-pin to 15-pin cable does not fit the Pi 5 |
| Screen | Ordered, waiting | iPistBit 4.3" DSI IPS capacitive touch screen, 800x480 | £16.17 delivered (listed £27.62, sale price) |

Prices are from search results and may have changed. None of the parts have been connected or tested yet.

## Pi 5 ports

| Port | Pi 5 has | Used | Free |
|---|---|---|---|
| USB | 2x USB 3.0, 2x USB 2.0 | none | all 4 (speaker and mic will use 2) |
| Micro HDMI | 2 | none | both |
| 22-pin CSI/DSI | 2 (each takes a camera or a display) | 1 (camera), 1 more when the screen arrives | 1 now, 0 after the screen |
| 3.5mm audio jack | none (removed on the Pi 5) | n/a | n/a |
| 40-pin GPIO | 1 | Robot HAT V4 | none |

Notes:
- Pi 5 CSI/DSI connectors are 22-pin, 0.5 mm pitch, smaller than the 15-pin ones on the Pi 3. A 15-pin DSI display needs a 22-to-15 adapter cable.
- The camera needs a 22-to-15 cable too. A new one is on order. Either CSI/DSI port works for the camera. If it is not detected, check the cable is not flipped at either end.
- On the Pi 5, camera tools are `rpicam-*` (not `raspistill`). `vilib` has not been checked against this yet.
- Not yet checked: whether the chassis or HAT physically blocks any ports.

## Speaker and microphone notes

- Both are plain USB audio devices, so they should work without drivers.
- The speaker is 2x2 W, 5 V, powered from USB, with a 116 cm cable. The Pi Hut says installing PulseAudio helps on recent Raspberry Pi OS.
- One reviewer saw their Pi reboot when audio played from this speaker, and a powered USB hub fixed it. If this happens, try a different USB port or a powered hub.
- Reviewers say cheap USB mics are quiet. Plan to raise the input gain in software.
- Keep the mic away from the speaker to avoid echo.
- The HAT's own I2S audio (GPIO18/19/21) is no longer used. Do not use those pins for anything else without checking.
- Software: the real `Speaker` will use USB audio, not the HAT. A `Microphone` HAL interface will be needed. See `docs/architecture.md`.

## Screen (ordered)

Chosen: the iPistBit 4.3" DSI IPS capacitive touch screen, 800x480, £16.17 delivered. It is bigger and cheaper than the Waveshare DSI screens below. Touch comes with it but is not needed.

Seller comments mostly say it works out of the box on a Pi 5, so the plan is to hope that is true. The listing's "no drivers needed" line is an AI summary, so it is not proof.

To check when it arrives:
- The cable. These screens usually ship with a 15-pin cable, and the Pi 5 port is 22-pin. If the box has no 22-pin cable, buy the display adapter cable in the table below.
- If the screen stays blank, the seller's page or wiki may give a `dtoverlay=` line to add to `/boot/firmware/config.txt`.
- Where it fits on the robot. The board is about 10 cm wide, and the chassis, HAT and fan may be in the way.
- Whether the screen's cable blocks the camera cable or any other port.

## Screen options considered

The screen could go on the Pi 5's free DSI port, a micro HDMI port, or the HAT's free headers. Only SPI (and I2C OLED) fit at around £10. I already have a small I2C OLED, but I want colour and a bigger screen.

| Option | Interface | Size and resolution | Listed price | Notes |
|---|---|---|---|---|
| [Waveshare 1.69" LCD](https://thepihut.com/products/1-69-lcd-display-module-240x280) | SPI (HAT) | 240x280, ST7789V2 | £9.40 | In stock when seen. Cheapest colour option |
| [Waveshare 2" IPS LCD](https://thepihut.com/products/2-ips-lcd-display-module-240x320) | SPI (HAT) | 240x320, ST7789 | £11.60 | Bigger. 8-pin cable included |
| [Waveshare 2.4" LCD](https://thepihut.com/products/2-4-lcd-display-module-240x320) | SPI (HAT) | 240x320, ILI9341 | not checked | Biggest SPI option. Pi Hut page was rate-limited, so check the price |
| [Waveshare 3.5" DSI](https://thepihut.com/products/3-5-dsi-capacitive-touch-display-for-raspberry-pi-640x480) | DSI (Pi 5) | 640x480, touch | £31.70 | Needs a 22-to-15 cable. Touch not needed but comes with it |
| [Waveshare 2.8" DSI](https://thepihut.com/products/2-8-ips-capacitive-touch-dsi-display-for-raspberry-pi-480x640) | DSI (Pi 5) | 480x640, touch | £42.30 | Pi 5 support unclear on the Pi Hut listing |
| [Display adapter cable](https://thepihut.com/products/display-adapter-cable-for-raspberry-pi-5) | n/a | 22-pin to 15-pin | about £1-2 | Needed for either DSI screen |

Findings:
- No non-touch DSI or HDMI screen between 2" and 3.5" was found at a UK shop. The smallest HDMI and DSI screens are 3.5" and cost over £30.
- AliExpress sells cheap SPI modules (for example a 2.4" ST7789) but not small HDMI or USB screens. UK VAT is added at checkout on orders up to £135, and delivery is slower. I could not see live AliExpress prices.
- If buying on AliExpress, check the driver chip (ST7789 or ILI9341), the pin count (7, 8 or 12), 3.3 V logic, and whether header pins are soldered on.

## Wiring a SPI screen to the Robot HAT V4

Only needed if the DSI screen does not work out and I fall back to an SPI screen.

Worked out from the HAT spec and not yet checked against the board. Check the physical pin order of the HAT's SPI and digital headers first.

| Screen pin | HAT connection | Pi GPIO |
|---|---|---|
| VCC | 3.3V on the SPI header | n/a |
| GND | GND on the SPI header | n/a |
| DIN (data) | MOSI on the SPI header | GPIO10 |
| CLK | SCK on the SPI header | GPIO11 |
| CS | CS on the SPI header | GPIO8 |
| DC | BSY on the SPI header | GPIO6 |
| RST | signal pin of the D0 header | GPIO17 |
| BL (backlight) | 3.3V (always on), or the D1 header signal pin | GPIO4 |

- Waveshare's example code uses GPIO25 (DC), GPIO27 (RST) and GPIO18 (BL). On this robot, GPIO25 is the USR button, GPIO27 is the ultrasonic TRIG (D2) and GPIO18 is I2S audio. The code needs the pin numbers changed to the ones above.
- Leave D2 and D3 alone. The ultrasonic sensor uses them.
- Needs about 8 female-to-female jumper wires, SPI enabled (`sudo raspi-config`, Interface Options, SPI), and the lgpio library on Bookworm. Not yet confirmed to work on the Pi 5.
- Waveshare's pin table is for the touch model of the 1.69" screen. Check the non-touch model's wiki before wiring.

## Open decisions

- Whether the DSI screen works on the Pi 5 and fits on the robot. If not, fall back to an SPI screen.
- Whether to add a `Display` HAL interface (and `Microphone`) to the architecture plan.
