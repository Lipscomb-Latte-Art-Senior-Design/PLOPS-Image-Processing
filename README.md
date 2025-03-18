# PLOPS Image Processing

This repository contains a collection of Python scripts for processing images and generating G-code for a machine that prints powder (cinnamon or cocoa) on the top of a coffe drink.

## Prototypes

Both prototypes of this machine are based on the Makerbot Replicator Mini+.

Prototype 1 used the built in control hardware and software of the Makerbot, so `mbotmake.py` was used to convert the G-code to a Makerbot-compatible format.

Prototype 2 uses an ATmega2560 microcontroller and a RAMPS 1.4 board to control the machine. The `post_process_ngc.py` script is used to convert the Inkscape-generated NGC file to a G-code file that can be run by the Marlin firmware.

## post_process_ngc.py
- **Purpose:**  
  This script post-processes an NGC file exported from Inkscape. The NGC file typically contains commands with comments and extra details that need conversion to a G-code format the Makerbot can use.
- **Functionality:**  
  - **Header, Cutting Paths, and Footer:**  
    It parses the input file by separating it into a header (pre-cutting), cutting paths (between start and end markers), and a footer (post-cutting).  
  - **Command Modifications:**  
    - Removes any extraneous comments.
    - Replaces specific Z coordinate values with predefined `PRINT_HEIGHT` and `TRAVEL_HEIGHT`.
    - Eliminates unnecessary feed rate commands.
    - Computes movement distances and appends these as inline comments for clarity.
    - Inserts commands to start and stop the vibrator, and adds a delay before travel.
- **Usage:**  
  To run the script for converting your NGC file to G-code:
  ```bash
  python3 post_process_ngc.py input.ngc output.gcode --print-height 97.0 --travel-height 103.0
  ```
  Adjust `--print-height` and `--travel-height` if necessary.
