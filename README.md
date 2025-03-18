# mbotmake

This repository is a fork of [mbotmake](https://github.com/sckunkle/mbotmake) with modifications specifically built for controlling a modified Makerbot Replicator Mini+ 3D Printer for alternate purposes.

Below you'll find a description of each Python file in the codebase and instructions on how to use them.

---

## File Descriptions

### mbotmake.py
- **Purpose:**  
  This is the main executable file of the project. It takes a G-code file as an input argument and processes it to control the Makerbot printer.
- **Usage:**  
  Run the script with the path to your G-code file as the first argument:
  ```bash
  python3 mbotmake.py /path/to/your/file.gcode
  ```
- **Supported G-code Commands:**  
  Only the following commands are supported: `G0/G1`, `G92`, `M104`, `M106`, `M107`, `M140`.

### makerbot_files.py
- **Purpose:**  
  This module provides helper functions related to the creation and management of metadata and command generation for the printer.  
  For example:
  - `generateMetajson(vardict)`: Produces a JSON string that contains metadata such as printing duration, extrusion details, temperature settings, and more. This JSON metadata is included with the G-code commands.
  - `generateCommand(function, metadata, parameters, tags)`: Builds individual command objects that encapsulate the action, parameters, and associated metadata.
  - Other functions (like `computeTime`) handle calculations (e.g., movement duration) that are necessary for synchronized printer operation.

### post_process_ngc.py
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

### makelinetest.py
- **Purpose:**  
  This script is designed for testing the printer’s response to linear commands. It helps verify that linear movements (typically represented by G0/G1 commands) are being executed correctly by printing test patterns.
- **Usage:**  
  Run the script without arguments to see a series of linear movement commands and associated diagnostics:
  ```bash
  python3 makelinetest.py
  ```
- **Notes:**  
  Use this script to debug or calibrate the printer’s linear movement functionality.

### makesmileyface.py
- **Purpose:**  
  This script generates a smiley face pattern as a G-code demonstration. It is useful for testing the printer’s capability to print curved and complex shapes and for a fun demonstration of the system.
- **Usage:**  
  Simply execute the script to generate and send the smiley face G-code to the printer:
  ```bash
  python3 makesmileyface.py
  ```
- **Notes:**  
  The generated pattern can be modified or used as a starting point for more complex designs.

### test_stream.py
- **Purpose:**  
  This script tests the streaming functionality of the G-code commands. It simulates and verifies the process of sending commands incrementally to the printer, ensuring that the streaming interface works as expected.
- **Usage:**  
  Run the script to initiate a test stream of commands:
  ```bash
  python3 test_stream.py
  ```
- **Notes:**  
  Utilize this script when debugging communication or processing issues related to G-code streaming.

---

## Getting Started

1. **Preparation:**  
   Make sure you have Python 3 installed on your system.

2. **Running the Main Program:**  
   Use `mbotmake.py` by passing the path to your G-code file:
   ```bash
   python3 mbotmake.py /path/to/your/file.gcode
   ```

3. **Post-processing NGC Files:**  
   If you are generating G-code from Inkscape and have an NGC file, convert it using:
   ```bash
   python3 post_process_ngc.py input.ngc output.gcode
   ```
   Adjust `--print-height` and `--travel-height` if necessary.

4. **Testing and Demonstrations:**  
   - Use `makelinetest.py` to verify linear movement commands.
   - Use `makesmileyface.py` to print a smiley face pattern as a demo.
   - Use `test_stream.py` to test the command streaming functionality.

---

## Limitations

- The system currently only supports the following G-code commands: `G0/G1`, `G92`, `M104`, `M106`, `M107`, `M140`.
- Make sure that your G-code file only contains these commands for successful processing.

---

## Additional Notes

- This repository is tailored for a modified Makerbot Replicator Mini+ and may not be directly compatible with other 3D printer models.
- The metadata generation (in `makerbot_files.py`) is hard-coded with certain printer specifications (e.g., bounding box dimensions, temperatures, material type). Adjust these values if you are adapting the codebase for another printer or purpose.

Enjoy printing, and feel free to contribute or modify the scripts to suit your specific needs!