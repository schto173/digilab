# Raspberry Pi I2C LCD Control Scripts

## Overview

This project provides a set of Python scripts for controlling a character-based I2C LCD (like a 16x2 or 20x4 display) connected to a Raspberry Pi. These scripts are designed to be modular and can be easily called from the command line or integrated into other applications, such as Node-RED flows.

The scripts typically interface with LCDs that use an I2C backpack based on the PCF8574 I/O expander chip.

## Features

*   **Modular Design:** Separate scripts for different LCD functions.
*   **Core LCD Class:** A base Python class (`base.py`) handles low-level I2C communication, which other scripts import.
*   **Initialization & Clear:** Script to initialize the LCD to a known state and clear its contents.
*   **Text Writing:** Script to write text to specific lines on the LCD.
*   **Backlight Control:** Script to turn the LCD backlight on or off.
*   **Cursor Control:** Script to set cursor position, and toggle cursor visibility and blink.
*   **Command-Line Interface:** All functional scripts are executable and accept command-line arguments.
*   **Node-RED Friendly:** Designed for easy integration with Node-RED using `Exec` and `Template` nodes.

## Hardware Requirements

*   Raspberry Pi (any model with GPIO pins).
*   I2C Character LCD Display (e.g., 16x2 or 20x4) with a PCF8574-based I2C backpack.
*   Jumper wires to connect the LCD to the Raspberry Pi's I2C pins.
    *   **SDA:** Connect to Raspberry Pi's SDA pin (GPIO 2).
    *   **SCL:** Connect to Raspberry Pi's SCL pin (GPIO 3).
    *   **VCC:** Connect to Raspberry Pi's 5V pin.
    *   **GND:** Connect to Raspberry Pi's GND pin.

## Software Requirements

*   **Raspberry Pi OS** (or any compatible Linux distribution).
*   **Python 3**.
*   **`python3-smbus` library:** For I2C communication.
*   **I2C enabled** on the Raspberry Pi.
*   (Optional) **Node-RED** if you plan to control the LCD via Node-RED flows.

## File Structure

The Python scripts are intended to be placed in a directory on your Raspberry Pi. For the examples in this README, we assume they are in `/home/tom/lcd/`. You should adapt paths accordingly if you place them elsewhere.