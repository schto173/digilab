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

/home/tom/lcd/
├── base.py # Core LCD communication class
├── init_clear.py # Script to initialize and clear the LCD
├── write_line.py # Script to write text to a specific line
├── backlight.py # Script to control the backlight
└── cursor.py # Script to control cursor position and appearance


## Python Scripts Details

### 1. `base.py`

*   **Purpose:** This script is not meant to be run directly. It defines the core `LCD` class that handles all low-level I2C communication with the LCD's PCF8574 I/O expander. It includes methods for sending bytes, toggling the enable pin, and managing the backlight state. Other functional scripts import this class.
*   **Key Configuration:**
    *   `LCD_ADDR`: The I2C address of your LCD. **You MUST verify and set this correctly.** Common addresses are `0x27` or `0x3F`. The scripts are pre-configured with `0x38` as per recent discussions.

### 2. `init_clear.py`

*   **Purpose:** Initializes the LCD to a standard 4-bit mode, sets display parameters (2 lines, 5x8 font), turns the display on (cursor and blink off by default), and clears the screen. It also sets the backlight on by default during initialization.
*   **Usage:**
    ```bash
    python /home/tom/lcd/init_clear.py
    ```
*   **Arguments:** None.

### 3. `write_line.py`

*   **Purpose:** Writes a string of text to a specified line on the LCD. The text will be padded with spaces or truncated to fit the LCD's line length (assumed to be 16 characters).
*   **Usage:**
    ```bash
    python /home/tom/lcd/write_line.py --line <line_number> --message "<your_message>"
    ```
*   **Arguments:**
    *   `--line`: (Required) The line number to write to. Integer, `1` or `2`.
    *   `--message`: (Required) The text string to display. Enclose in quotes if it contains spaces.

*   **Example:**
    ```bash
    python /home/tom/lcd/write_line.py --line 1 --message "Hello World!"
    python /home/tom/lcd/write_line.py --line 2 --message "RasPi LCD Test"
    ```

### 4. `backlight.py`

*   **Purpose:** Turns the LCD backlight on or off.
*   **Usage:**
    ```bash
    python /home/tom/lcd/backlight.py <state>
    ```
*   **Arguments:**
    *   `state`: (Required) Desired backlight state. String, `on` or `off`.

*   **Example:**
    ```bash
    python /home/tom/lcd/backlight.py on
    python /home/tom/lcd/backlight.py off
    ```

### 5. `cursor.py`

*   **Purpose:** Controls the LCD cursor's position, visibility, and blink status. It can also turn the entire display on or off.
*   **Usage:**
    ```bash
    python /home/tom/lcd/cursor.py [options]
    ```
*   **Arguments (all optional):**
    *   `--line <line_number>`: Set cursor line. Integer, `1` or `2`.
    *   `--col <column_number>`: Set cursor column. Integer, `0` to `15`. Requires `--line` if used.
    *   `--display <state>`: Turn display ON or OFF. String, `on` or `off`.
    *   `--cursor <state>`: Turn cursor visibility ON or OFF. String, `on` or `off`.
    *   `--blink <state>`: Turn cursor blink ON or OFF. String, `on` or `off`.

*   **Examples:**
    ```bash
    # Move cursor to Line 2, Column 5
    python /home/tom/lcd/cursor.py --line 2 --col 5

    # Turn cursor visibility on
    python /home/tom/lcd/cursor.py --cursor on

    # Turn cursor blink on (cursor must also be on to see blink)
    python /home/tom/lcd/cursor.py --cursor on --blink on

    # Turn display off
    python /home/tom/lcd/cursor.py --display off

    # Reset to display on, cursor off, blink off
    python /home/tom/lcd/cursor.py --display on --cursor off --blink off
    ```

## Setup and Installation

1.  **Clone the Repository (or Copy Files):**
    If this is a Git repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    # Then copy scripts to your desired location, e.g., /home/tom/lcd/
    # mkdir -p /home/tom/lcd
    # cp *.py /home/tom/lcd/
    ```
    If you have the files directly, create the directory and copy them:
    ```bash
    mkdir -p /home/tom/lcd
    # Copy base.py, init_clear.py, etc. into /home/tom/lcd/
    ```

2.  **Enable I2C on Raspberry Pi:**
    *   Run `sudo raspi-config`.
    *   Navigate to `Interface Options` (or `Advanced Options` on older versions).
    *   Select `I2C` and enable it.
    *   Reboot if prompted.

3.  **Install `python3-smbus`:**
    ```bash
    sudo apt-get update
    sudo apt-get install python3-smbus
    ```

4.  **Identify LCD I2C Address:**
    Connect your LCD to the Raspberry Pi's I2C pins (SDA, SCL, 5V, GND).
    Run the following command to detect connected I2C devices:
    ```bash
    sudo i2cdetect -y 1
    ```
    (If you are using an older Raspberry Pi Model B Rev 1, use `i2cdetect -y 0`).
    You should see a number in the grid (e.g., `27`, `3f`, or `38`). This is your LCD's I2C address in hexadecimal.

5.  **Configure `LCD_ADDR` in `base.py`:**
    Open `/home/tom/lcd/base.py` with a text editor:
    ```bash
    nano /home/tom/lcd/base.py
    ```
    Find the line:
  
python
Copy Code
LCD_ADDR = 0x38 # <<< MAKE SURE THIS IS CORRECT
Change `0x38` to the hexadecimal address you found in the previous step (e.g., `0x27`). Save the file.
6. Make Scripts Executable:
Navigate to the directory containing the scripts and make them executable:
bash       cd /home/tom/lcd/       chmod +x *.py     
(Note: base.py doesn't strictly need to be executable as it's a library, but it doesn't hurt.)

Usage
Directly from Command Line
After setup, you can run the scripts directly from the terminal as shown in the "Python Scripts Details" section.

Recommended first steps:

Initialize and clear the display:
bash
Copy Code
python /home/tom/lcd/init_clear.py
Write some text:
bash
Copy Code
python /home/tom/lcd/write_line.py --line 1 --message "Setup OK!"
python /home/tom/lcd/write_line.py --line 2 --message "LCD is working."
Integration with Node-RED
These scripts are ideal for use with Node-RED on your Raspberry Pi.

Exec Node: Use the Exec node in Node-RED to run the Python scripts.
Template Node: For scripts that require arguments (like write_line.py, backlight.py, cursor.py), you can use a Template node to construct the full command string. The Template node can take input from msg.payload (e.g., a JSON object containing the message and line number) and format it into the command.
Conceptual Node-RED Flow for Writing Text:

Inject Node (configured to send a JSON payload like {"line": 1, "message": "From Node-RED"})
-> Template Node (builds the command string: python /home/tom/lcd/write_line.py --line "{{payload.line}}" --message "{{payload.message}}")
-> Exec Node (runs the command from the template node's output)
-> Debug Node (to see script output/errors)
Example Template node content for write_line.py:

handlebars
Copy Code
python /home/tom/lcd/write_line.py --line "{{payload.line}}" --message "{{payload.message}}"
Make sure the "Output" format of the Template node is set to "Plain text". The Exec node should have its "Append msg.payload to command" option unchecked if the full command is generated by the Template node and passed in msg.payload. Alternatively, if the Exec node's command field is empty and "Append msg.payload" is checked, the Template node's output (the command string) should be in msg.payload.

Example Inject node for init_clear.py:
Set msg.payload (string) to: python /home/tom/lcd/init_clear.py
Connect directly to an Exec node (with "Append msg.payload" checked and command field empty, or command field set to msg.payload and append unchecked).

Troubleshooting
IOError: [Errno 2] No such file or directory (when running script):
Ensure you are using the correct full path to the Python script.
Check that the Python interpreter (python or python3) is correctly specified or in your PATH. Using python3 /path/to/script.py is often more explicit.
IOError: [Errno 5] Input/output error (from smbus):
Wrong I2C Address: Double-check LCD_ADDR in base.py matches the output of i2cdetect -y 1.
Wiring Issues: Verify SDA, SCL, VCC, and GND connections are secure and correct.
I2C Not Enabled: Ensure I2C is enabled via raspi-config.
Permissions: Running scripts with sudo (e.g., sudo python /path/to/script.py) can sometimes resolve permission issues with I2C, though ideally, your user should be part of the i2c group (sudo usermod -aG i2c your_username, then log out and back in).
LCD shows blocks or garbage characters:
Often an initialization timing issue or incorrect initialization sequence. The provided init_clear.py should work for most PCF8574-based displays.
Could also be a power issue. Ensure the Raspberry Pi can supply enough current.
Backlight works, but no text:
Check the contrast potentiometer on the LCD backpack (if it has one). It might need adjustment.
Verify I2C address and wiring.
Customization
LCD I2C Address: The most common customization is changing LCD_ADDR in base.py.
PCF8574 Pin Mappings: The base.py script assumes a common pin mapping for PCF8574 backpacks (RS, E, Backlight, D4-D7). If your backpack has a different mapping, you would need to adjust the bitwise operations and pin constants (RS_PIN_VAL, EN_PIN_VAL, BACKLIGHT_PIN_VAL) in base.py. This is an advanced modification.
Timing Constants: E_PULSE and E_DELAY in base.py can be adjusted if you face issues, but the defaults are usually fine.
Contributing
Contributions are welcome! If you have improvements, bug fixes, or new features:

Fork the repository.
Create a new branch (git checkout -b feature/YourFeature).
Make your changes.
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature/YourFeature).
Open a Pull Request.
License
This project is licensed under the MIT License - see the LICENSE file for details (if you choose to add one).


**Next Steps for You:**

1.  **Save this content:** Copy the text above and save it as `README.md` in the root of your GitHub repository (or the directory where you plan to put these scripts).
2.  **Create a `LICENSE` file (Optional but Recommended):** If you want to use the MIT license, create a file named `LICENSE` (or `LICENSE.md`) in the same directory with the following content:

    ```
    MIT License

    Copyright (c) [Year] [Your Name or GitHub Username]

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    ```
    Replace `[Year]` and `[Your Name or GitHub Username]`.
3.  **Review and Adapt:** Read through the `README.md` and make sure all paths and instructions accurately reflect your setup or provide clear guidance for other users to adapt them.
4.  **Push to GitHub:** Add, commit, and push your `README.md`, `LICENSE` (if created), and Python script files to your GitHub repository.