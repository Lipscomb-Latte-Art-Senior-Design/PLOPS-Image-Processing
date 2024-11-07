# NOTE
This repository is a fork from [here](https://github.com/sckunkle/mbotmake) to specifically control a modified Makerbot Replicator Mini+ 3D Printer for an alternate purpose.

# How to Run
Run mbotmake with the path to your .gcode file as the first argument.

    python3 mbotmake.py /path/to/your/file.gcode 


# Limitations
These are the only support gcode commands: G0/G1, G92, M104, M106, M107, M140