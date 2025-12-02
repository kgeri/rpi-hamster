# Rpi-Hamster

This repo has build instructions and code for a toy hamster based on a Raspberry Pi 2350.
Like 90's Tamagotchi, the purpose is to teach my son about the difficulties and responsibilities of owning a pet 😊

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
