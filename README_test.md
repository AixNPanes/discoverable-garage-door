# Test bed setup

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Prerequisites](#prerequisites)
  - [Install the module if you haven't already](#install-the-module-if-you-havent-already)
  - [Run the module](#run-the-module)
  - [Create a button helper](#create-a-button-helper)
  - [Create your Button](#create-your-button)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Hardware

- Raspberry Pi Zero W
- 2 Channel 5V Relay Board for Raspberry Pi - SB Components SKU14088
- Breadboard
- 2 slide switches
- LED
- 220Ω resistor
- miscellaneous jumpers

## Connections

![image info](./images/TestBed.png)

## Software

- Raspian OS (Debian Bullseye or newer)
- Python 3.11 (Currently only install-from-source is available), go to https://www.python.org/downloads/ to the most current version and use that in the following export
```
    export VERSION=3.11.4
    sudo apt-get update
    sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
    cd ~/Downloads
    wget https://www.python.org/ftp/python/${VERSION}/Python-${VERSION}.tgz
    tar zxf Python-${VERSION}.tgz
    cd Python-${VERSION}
    ./configure --enable-optimizations
    sudo make altinstall
```
- discoverable-garage-door
  - install to ~/.local/lib

    python3.11 pip install discoverable-garage-door

  - install to /usr/local/lib/python3.11/site-packages/

    sudo python3.11 pip install discoverable-garage-door

## Test

python3.11 -m discoverable_garage_door
