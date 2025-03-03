import serial
import time
import serial.tools.list_ports
import sys
import os

def find_serial_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        device = port.device.lower() if port.device else ""
        description = port.description.lower() if port.description else ""
        if ("cu.usbmodem" in device or 
            "tty.usbmodem" in device or 
            "arduino" in description or 
            "atmel" in description or 
            "usb serial" in description):
            return port.device
    # Fallback: if no match is found, return the first available port
    if ports:
        return ports[0].device
    return None

def wait_for_ok(ser):
    """Reads lines from the serial port until an 'ok' is received."""
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            print(f"Received: {line}")
        if "ok" in line.lower():
            break

def stream_gcode(filepath, ser):
    try:
        with open(filepath, 'r') as f:
            commands = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print("Ready to stream commands. Press Enter to begin...")
    input()

    for idx, cmd in enumerate(commands):
        # Clean up the command (remove whitespace/newlines)
        cmd = cmd.strip()
        if not cmd or cmd.startswith(";"):  # skip empty lines or comments
            continue

        # Send command to printer
        command_str = cmd + "\r\n"
        print(f"Sending command {idx+1}: {cmd}")
        ser.write(command_str.encode('utf-8'))

        # Wait until the printer responds with "ok"
        wait_for_ok(ser)

def main():
    # Check for filepath argument
    if len(sys.argv) < 2:
        print("Usage: python stream_gcode.py <path_to_gcode_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    # Find the serial port
    serial_port = find_serial_port()
    if serial_port is None:
        print("Serial port not found")
        sys.exit(1)

    baudrate = 250000

    try:
        ser = serial.Serial(serial_port, baudrate, timeout=2)
    except Exception as e:
        print(f"Failed to open serial port: {e}")
        sys.exit(1)

    print(f"Serial port {serial_port} open with baudrate {baudrate}.")
    # Wait for the printer to initialize and send initial messages if any.
    time.sleep(5)

    # Start streaming gcode commands
    stream_gcode(filepath, ser)

    print("Finished streaming commands.")
    ser.close()

if __name__ == "__main__":
    main()