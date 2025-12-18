# Rpi-Hamster

This repo has build instructions and code for a toy hamster based on a Raspberry Pi 2350.
Like 90's Tamagotchi, the purpose is to teach my son about the difficulties and responsibilities of owning a pet 😊

## Features

* [✔️] Showing faces on the LCD display
* [✔️] Touch detection (pet and feed)
* [✔️] Gyro detection (scared, happy, dropped)
* [✔️] Piezo sounds (welcome, squeak)
* [✔️] Battery indicator (voltage, primitive charging detection)
* [✔️] GC watchdog and error.log ([RingBuffer](src/lib/logging.py))
* [❌] Calibrate battery percentage, battery menu (?)
* [❌] Improve gyro / drop detection (multi-sample)
* [❌] Power saving mode, wake up on use
* [❌] Sleep schedule, wake up at night
* [❌] Cage cleaning reminder?
* [❌] Documented build, body

## Hardware

[RP2350 MCU Board, With 1.28inch Round Touch LCD](docs/RP2350_Round_Touch_LCD.md)

## Development

VSCode plugins:

* [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)
* [pico-vscode](https://marketplace.visualstudio.com/items?itemName=raspberry-pi.raspberry-pi-pico)

Python setup:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

* Build & deploy: `./deploy.sh`
* Debug: `mpremote`
* REPL: `mpremote repl`
