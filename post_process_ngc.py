#!/usr/bin/env python3
"""
post_process_ngc.py

This script converts an NGC file exported from Inkscape (which contains comments in parentheses)
into a G-code file formatted for Marlin firmware. It separates the input into a header (lines before any cutting path),
cutting paths (between the start and end markers), and a footer (lines after the footer marker),
removing original comments and then performing some modifications, such as replacing specific Z values,
removing extraneous feed rate commands, and computing movement distances with extrusion commands.

The generated G-code file wraps the header, each cutting path (with a sequential ID), and the footer
with custom begin/end comments. Movement commands (G00/G01/G02/G03) have a computed distance appended
as an inline comment. Also, the script inserts commands to start and stop the vibrator and delay before travel.

Usage:
    python3 post_process_ngc.py input.ngc output.gcode [--print-height PRINT_HEIGHT] [--travel-height TRAVEL_HEIGHT]

Parameters:
    input.ngc       Input NGC file.
    output.gcode    File where the post-processed G-code is saved.
    --print-height  Value used to replace "Z0.000000" (default: 97.0).
    --travel-height Value used to replace "Z5.000000" (default: 103.0).
"""

import re
import sys
import math
import argparse

# Global configuration constants.
PRINT_HEIGHT = 97.0
TRAVEL_HEIGHT = 103.0
VIBRATOR_SPEED = 80
TRAVEL_DELAY_MS = 50

# These are the parameter for the extrusion curve pulled from the desmos graph.
# https://www.desmos.com/calculator/8ubo1wfgou
EXTRUSION_CURVE_a = (y3-y0)/(x3-x0)
EXTRUSION_CURVE_x0 = 0
EXTRUSION_CURVE_x1 = 118.1
EXTRUSION_CURVE_x2 = 59.2
EXTRUSION_CURVE_x3 = 155
EXTRUSION_CURVE_y0 = 0.05
EXTRUSION_CURVE_y1 = 0.05
EXTRUSION_CURVE_y2 = 0.58
EXTRUSION_CURVE_y3 = 1.575

def extrusion_curve(t):
    """
    Calculate the extrusion curve value for a given t value. This is a cubic Bezier curve.
    """
    return (
        (1-t)*((1-t)*((1-t)*EXTRUSION_CURVE_x0 + t*EXTRUSION_CURVE_x1) + t*((1-t)*EXTRUSION_CURVE_x1 + t*EXTRUSION_CURVE_x2))
        + t*((1-t)*((1-t)*EXTRUSION_CURVE_x1 + t*EXTRUSION_CURVE_x2) + t*((1-t)*EXTRUSION_CURVE_x2 + t*EXTRUSION_CURVE_x3)),
        (1-t)*((1-t)*((1-t)*EXTRUSION_CURVE_y0 + t*EXTRUSION_CURVE_y1) + t*((1-t)*EXTRUSION_CURVE_y1 + t*EXTRUSION_CURVE_y2))
        + t*((1-t)*((1-t)*EXTRUSION_CURVE_y1 + t*EXTRUSION_CURVE_y2) + t*((1-t)*EXTRUSION_CURVE_y2 + t*EXTRUSION_CURVE_y3))
    ) if t >= EXTRUSION_CURVE_x0 and t <= EXTRUSION_CURVE_x3 else EXTRUSION_CURVE_a * (t - EXTRUSION_CURVE_x0) + EXTRUSION_CURVE_y0

def replace_z_and_feed(line):
    """
    Replace specific Z coordinate values and remove feed rate commands.
    
    Replaces:
        - "Z0.000000" with PRINT_HEIGHT.
        - "Z5.000000" with TRAVEL_HEIGHT.
        - Removes "F4000.0" and "F4000.000000".
    
    Args:
        line (str): An input line from the NGC file.
    
    Returns:
        str: The modified line.
    """
    line = line.replace("Z0.000000", f"Z{PRINT_HEIGHT}")
    line = line.replace("Z5.000000", f"Z{TRAVEL_HEIGHT}")
    line = line.replace("F4000.0", "")
    line = line.replace("F4000.000000", "")
    return line

def modify_command(cmd, current_position):
    """
    Modify a single G-code movement command by removing inline comments, replacing Z values,
    computing the path length, and appending extrusion and length comments.

    Args:
        cmd (str): The original G-code command.
        current_position (dict or None): The current position as a dictionary with keys "X", "Y", "Z".

    Returns:
        tuple: (modified command as str, updated current_position as dict)
    """
    # Remove any inline comment (anything within parentheses at the end).
    m = re.search(r"(.*?)\s*\([^)]*\)\s*$", cmd)
    command_part = m.group(1).strip() if m else cmd.strip()

    # Determine if the command is a movement command (G00, G01, G02 or G03).
    code_match = re.match(r"(G0[0-3])", command_part, re.IGNORECASE)
    if not code_match:
        # Not a movement command: return as is.
        return command_part, current_position

    code = code_match.group(1).upper()

    def get_param(text, letter):
        pattern = letter + r"([-+]?[0-9]*\.?[0-9]+)"
        m_param = re.search(pattern, text, re.IGNORECASE)
        return float(m_param.group(1)) if m_param else None

    x = get_param(command_part, "X")
    y = get_param(command_part, "Y")
    z = get_param(command_part, "Z")
    i_val = get_param(command_part, "I")
    j_val = get_param(command_part, "J")

    if current_position is None:
        current_position = {"X": 0.0, "Y": 0.0, "Z": 0.0}

    length = 0.0
    new_position = current_position.copy()

    if code in ["G00", "G01"]:
        new_x = x if x is not None else current_position["X"]
        new_y = y if y is not None else current_position["Y"]
        new_z = z if z is not None else current_position["Z"]
        dx = new_x - current_position["X"]
        dy = new_y - current_position["Y"]
        dz = new_z - current_position["Z"]
        length = math.sqrt(dx*dx + dy*dy + dz*dz)
        new_position["X"] = new_x
        new_position["Y"] = new_y
        new_position["Z"] = new_z

    elif code in ["G02", "G03"]:
        # For arc movements, compute the arc length.
        if x is not None and y is not None and i_val is not None and j_val is not None:
            start_x = current_position["X"]
            start_y = current_position["Y"]
            end_x = x
            end_y = y
            center_x = start_x + i_val
            center_y = start_y + j_val
            radius = math.sqrt(i_val**2 + j_val**2)
            v1x = start_x - center_x
            v1y = start_y - center_y
            v2x = end_x - center_x
            v2y = end_y - center_y
            dot = v1x * v2x + v1y * v2y
            cross = v1x * v2y - v1y * v2x
            angle = abs(math.atan2(cross, dot))
            length = radius * angle
            new_position["X"] = end_x
            new_position["Y"] = end_y
            new_position["Z"] = z if z is not None else current_position["Z"]
        else:
            # If parameters for arc are missing, update any available coordinate.
            if x is not None:
                new_position["X"] = x
            if y is not None:
                new_position["Y"] = y
            if z is not None:
                new_position["Z"] = z

    # Compute extrusion amounts.
    extrusion_amount = extrusion_curve(length)

    extrusion_param = f"E{extrusion_amount:.3f}"
    length_comment = f"% length: {length:.3f}"

    # Append the extrusion parameter only for specific movement commands.
    if not re.match(r"(G0[1-3])", command_part, re.IGNORECASE):
        extrusion_param = ""

    new_cmd = f"{command_part} {extrusion_param} {length_comment}"
    return new_cmd, new_position

def parse_ngc_file(filename):
    """
    Parse an NGC file into its three sections: header, cutting paths, and footer.
    During the parsing process, all original comments are removed.
    For header and footer lines, Z coordinate values are replaced.

    Args:
        filename (str): Path to the NGC file.

    Returns:
        tuple: (header_lines, paths, footer_lines)
            header_lines (list of str): Commands in the header.
            paths (list of dict): Each dict contains a list of commands for a cutting path.
            footer_lines (list of str): Commands in the footer.
    """
    header_lines = []
    paths = []
    footer_lines = []
    current_path = None
    current_position = None
    in_header = True
    in_footer = False

    with open(filename, 'r') as f:
        for line in f:
            stripped = line.rstrip("\n").strip()
            if not stripped or stripped == "%":
                continue

            # Replace specific Z coordinates and feed commands.
            stripped = replace_z_and_feed(stripped)

            # Check for footer marker.
            if stripped == "(Footer)":
                in_footer = True
                in_header = False
                continue

            # Identify start of a cutting path.
            if re.match(r"\(Start cutting path id:", stripped, re.IGNORECASE):
                in_header = False
                in_footer = False
                if current_path is not None:
                    paths.append(current_path)
                current_path = {"commands": []}
                current_position = None
                continue

            # Identify the end of a cutting path.
            if re.match(r"\(End cutting path id:", stripped, re.IGNORECASE):
                if current_path is not None:
                    paths.append(current_path)
                    current_path = None
                continue

            # Skip any other complete comment line.
            if stripped.startswith("(") and stripped.endswith(")"):
                continue

            # Process and assign the command line to its section.
            if in_footer:
                footer_lines.append(stripped)
            elif current_path is not None:
                modified_cmd, current_position = modify_command(stripped, current_position)
                current_path["commands"].append(modified_cmd)
            elif in_header:
                header_lines.append(stripped)
            else:
                # Any stray lines default to the header.
                header_lines.append(stripped)
    return header_lines, paths, footer_lines

def write_gcode_file(filename, header, paths, footer):
    """
    Write the final G-code file with a wrapped header, each cutting path with additional markers,
    and a wrapped footer.

    Args:
        filename (str): The output file path.
        header (list of str): Header G-code lines.
        paths (list of dict): List of cutting paths, each containing a list of commands.
        footer (list of str): Footer G-code lines.
    """
    with open(filename, 'w') as f:
        # Write header block.
        f.write("% ======================== Begin header ========================\n")
        for line in header:
            f.write(line + "\n")
        f.write("% ======================== End header ========================\n\n")

        # Write each cutting path block with a sequential ID.
        for i, path in enumerate(paths, start=1):
            new_id = f"path {i:02d}"
            f.write(f"% ======================== Begin {new_id} ========================\n")
            wrote_path_header = False
            for cmd in path["commands"]:
                if re.match(r"(G0[1-3])", cmd, re.IGNORECASE):
                    if not wrote_path_header:
                        f.write(f"M106 S{VIBRATOR_SPEED} % Start Vibrator\n")
                        wrote_path_header = True
                f.write(cmd + "\n")
            f.write("M107 % Stop Vibrator\n")
            f.write(f"G4 P{TRAVEL_DELAY_MS} % Wait {TRAVEL_DELAY_MS}ms before travel\n")
            f.write(f"% ======================== End {new_id} ========================\n\n")

        # Write footer block.
        f.write("% ======================== Begin footer ========================\n")
        for line in footer:
            f.write(line + "\n")
        f.write("% ======================== End footer ========================\n\n")
        f.write("%\n")

def main():
    """
    Main function to handle argument parsing, processing of the NGC file,
    and writing the final G-code output.
    """
    global PRINT_HEIGHT, TRAVEL_HEIGHT
    parser = argparse.ArgumentParser(
        description="Process an NGC file to produce G-code formatted for Marlin firmware."
    )
    parser.add_argument("input", help="Input NGC file")
    parser.add_argument("output", help="Output G-code file")
    parser.add_argument("--print-height", type=float, default=PRINT_HEIGHT,
                        help=f"Print height (replaces Z0.000000). Default: {PRINT_HEIGHT}")
    parser.add_argument("--travel-height", type=float, default=TRAVEL_HEIGHT,
                        help=f"Travel height (replaces Z5.000000). Default: {TRAVEL_HEIGHT}")
    args = parser.parse_args()

    PRINT_HEIGHT = args.print_height
    TRAVEL_HEIGHT = args.travel_height

    # Parse the input NGC file into header, paths, and footer.
    header, paths, footer = parse_ngc_file(args.input)

    # The header is replaced with a standard set of commands.
    header = [
        "G28 % Auto Home",
        "M83 % Set Extruder to Relative Mode",
        "M107 % Turn off Vibrator",
        "",
        "% Actual Center: (X: 55.0, Y: 59.0)",
        "% \"Printing\" Center: (X: 58.0, Y: 59.0)",
        "% We offset by 3mm in the X to account for the horizontal velocity of the",
        "% powder coming out of the nozzle.",
        "",
        "% Move to Actual Center",
        "% This is so the user can center the cup.",
        "G1 X55.0 Y59.0 Z103.0 F10000",
        "% G4 P1000 % Wait for move to finish",
        "% M117 Place your cup.",
        "% G4 P10000 % Wait 10000ms for user to place cup",
        "M117 Printing...",
    ]
    footer = [
        "% Presentation Position",
        "G1 X0.0 Y107.0 Z110.0",
        "M117 Enjoy"
    ]

    write_gcode_file(args.output, header, paths, footer)
    print(f"Post-processed G-code written to {args.output}")

if __name__ == "__main__":
    main()