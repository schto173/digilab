# /home/tom/lcd/write.py
from base import (LCD, LCD_CHR_MODE, LCD_CMD_MODE,
                      LCD_LINE_1_ADDR_BASE, LCD_LINE_2_ADDR_BASE)
import argparse

def main():
    parser = argparse.ArgumentParser(description="Write text to a specific line on an I2C LCD.")
    parser.add_argument("--line", required=True, type=int, choices=[1, 2], help="Line number (1 or 2).")
    parser.add_argument("--message", required=True, type=str, help="Message to display (max 16 chars).")
    args = parser.parse_args()

    try:
        lcd = LCD() # Assumes LCD is initialized, backlight state is managed by LCD object

        line_addr_base = LCD_LINE_1_ADDR_BASE if args.line == 1 else LCD_LINE_2_ADDR_BASE

        print(f"Python script (write_line): Writing to line {args.line}: '{args.message}'")

        lcd.lcd_byte(line_addr_base, LCD_CMD_MODE) # Set cursor to beginning of the line

        message_to_write = args.message.ljust(16," ") # Pad/truncate to 16 chars
        for char_code in [ord(c) for c in message_to_write]:
            lcd.lcd_byte(char_code, LCD_CHR_MODE)

        print("Python script (write_line): Write complete.")
    except Exception as e:
        print(f"Python script (write_line) error: {e}")

if __name__ == '__main__':
    main()