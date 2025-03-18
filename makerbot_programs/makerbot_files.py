import zipfile
import json
import sys
import tempfile
import copy
import math
import re
import traceback


def generateMetajson(vardict):
    meta = """
{{
    "duration_s": {4}, 
    "total_commands": {5},
    "bot_type": "mini_4",
    "bounding_box": {{
        "x_max": 13.9849853515625,
        "x_min": -13.9849853515625,
        "y_max": 13.9850001475781,
        "y_min": -13.98498535156251,
        "z_max": 11.58000000000001,
        "z_min": 0.15
    }},
    "chamber_temperature": null,
    "commanded_duration_s": {5},
    "extruder_temperature": 180,
    "extruder_temperatures": [
        180
    ],
    "extrusion_distance_mm": 420.0,
    "extrusion_distances_mm": [
        420.0
    ],
    "extrusion_mass_g": 69.0,
    "extrusion_masses_g": [
        69.0
    ],
    "grue_version": "5.14.0",
    "material": "pla",
    "materials": [
        "pla"
    ],
    "model_counts": [
        {{
            "count": 1,
            "name": "default"
        }}
    ],
    "num_z_layers": 56,
    "num_z_transitions": 55,
    "platform_temperature": 0,
    "preferences": {{
        "default": {{
            "overrides": {{
                "baseLayer": "raft"
            }},
            "print_mode": "balanced"
        }}
    }},
    "tool_type": "mk13",
    "tool_types": [
        "mk13"
    ],
    "uuid": "b7e64298-2066-46ce-b89f-719051c34ef2",
    "version": "1.2.0"
}}
    """
    meta = meta.format(vardict['tool0temp'], vardict['tool1temp'],
                       vardict['bedtemp'],
                       'true' if vardict['heatbed'] else 'false',
                       int(math.ceil(vardict['time'])),
                       vardict['toolpathfilelength'])
    return meta


def generateCommand(function, metadata, parameters, tags):
    return copy.deepcopy([
        {'command': {
            'function': function,
            'parameters': parameters,
            'metadata': metadata,
            'tags': tags
            }
        }
    ])


def computeTime(prev, current):
    if [current['x'], current['y'], current['z']] == [prev['x'], prev['y'], prev['z']] and current['a'] != prev['a']:
        # retraction takes time as well, add it in
        # time = sqrt((e2-e1)^2)/feedrate
        distance = math.dist([current['a']], [prev['a']])
    else:
        # get time traveled by the equasion
        # time = sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)/feedrate
        distance = math.dist([current['x'], current['y'], current['z']],
                             [prev['x'], prev['y'], prev['z']])
    return distance/current['feedrate']

def createToolpath(gcode_lines):
    corpus = gcode_lines # open(filename).readlines()
    processed = []
    linenum = 0
    axis = \
        {
            'a': 0.0,
            'feedrate': 0.0,
            'x': 0.0,
            'y': 0.0,
            'z': 0.0
        }
    tempmetadata = \
        {
            'index': -1,
            'temperature': 0
        }
    fanstatus = \
        {
            'index': 0,
            'value': False
        }
    fanduty = \
        {
            'index': 0,
            'value': 0.0
        }
    printersettings = \
        {
            'tool0temp': 40,
            'tool1temp': 0,
            'bedtemp': 0,
            'heatbed': False,
            'time': 0.0,
            'toolpathfilelength': 0
        }
    printeroffset = \
        {
            'a': 0.0,
            'x': 0.0,
            'y': 0.0,
            'z': 0.0
        }
    """
    Quick reference:
    G0/G1 is move
    M104 is set_toolhead_temperature
    M140 sets bed temp
    M106 is fan_duty (sets fan)
    M107 is toggle_fan (off)
    M141 sets chamber temperature
    G90 toggles absolute positioning
    G91 toggles relative positioning
    """
    for line in corpus:
        if line.find(';') > -1:
            line = line[:line.find(';')]
        line = [part for part in line.split(' ') if part != '']
        if len(line) == 0:  # Most likely a blank line
            linenum += 1
            continue
        if line[0] in ['G0', 'G1']:
            if len(line) == 2 and line[1][0] == 'F':
                axis['feedrate'] = float(line[1][1:]) / 60.0
            else:  # Normal move
                prev = copy.copy(axis)  # copy previous pos for timing
                for ax in line[1:]:
                    if ax[0] == 'E':
                        axis['a'] = printeroffset['a'] + float(ax[1:])
                    elif ax[0] == 'X':
                        axis['x'] = printeroffset['x'] + float(ax[1:])
                    elif ax[0] == 'Y':
                        axis['y'] = printeroffset['y'] + float(ax[1:])
                    elif ax[0] == 'Z':
                        axis['z'] = printeroffset['z'] + float(ax[1:])
                    elif ax[0] == 'F':
                        axis['feedrate'] = float(ax[1:]) / 60.0
                processed += generateCommand('move',
                                            {'relative':{
                                                'a': False,
                                                'x': False,
                                                'y': False,
                                                'z': False
                                            }},
                                            axis,
                                            [])
                printersettings['time'] += computeTime(prev, axis)
        elif line[0] == 'G92':
            for ax in line[1:]:
                if ax[0] == 'E':
                    printeroffset['a'] = axis['a'] + float(ax[1:])
                elif ax[0] == 'X':
                    printeroffset['x'] = axis['x'] + float(ax[1:])
                elif ax[0] == 'Y':
                    printeroffset['y'] = axis['y'] + float(ax[1:])
                elif ax[0] == 'Z':
                    printeroffset['z'] = axis['z'] + float(ax[1:])
        elif line[0] == 'M104':
            for ax in line[1:]:
                if ax[0] == 'T':
                    tempmetadata['index'] = int(ax[1:])
                elif ax[0] == 'S':
                    tempmetadata['temperature'] = int(ax[1:])
            if tempmetadata['index'] != -1:
                processed += generateCommand('set_toolhead_temperature',
                                            {},
                                            tempmetadata,
                                            [])
                if printersettings['tool{}temp'.format(tempmetadata['index'])] == 0:
                    printersettings['tool{}temp'.format(tempmetadata['index'])] = tempmetadata['temperature']
            else: # there is only one extruder
                processed += generateCommand('set_toolhead_temperature',
                                            {},
                                            {'temperature': tempmetadata['temperature']},
                                            [])
                printersettings['tool0temp'] = tempmetadata['temperature']
        elif line[0] == 'M106':
            for ax in line[1:]:
                if ax[0] == 'P':
                    fanduty['index'] = int(ax[1:])
                    fanstatus['index'] = int(ax[1:])
                elif ax[0] == 'S':
                    fanduty['value'] = float(ax[1:]) / 255
            if not fanstatus['value']:
                fanstatus['value'] = True
                processed += generateCommand('toggle_fan',
                                            {},
                                            fanstatus,
                                            [])
            processed += generateCommand('fan_duty',
                                        {},
                                        fanduty,
                                        [])
        elif line[0] == 'M107':
            fanstatus['value'] = False
            processed += generateCommand('toggle_fan',
                                        {},
                                        fanstatus,
                                        [])
        elif line[0] == 'M140':
            printersettings['bedtemp'] = int(line[1][1:])
            printersettings['heatbed'] = True
        linenum += 1

    compiledtoolpath = json.dumps(processed, sort_keys=False, indent=4)
    printersettings['toolpathfilelength'] = len(processed)

    return (compiledtoolpath, printersettings)

    # return printersettings


def packageMBotFile(filename, temp):
    with zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED) as mbotfile:
        mbotfile.write('{}/meta.json'.format(temp), arcname='meta.json')
        mbotfile.write('{}/print.jsontoolpath'.format(temp), arcname='print.jsontoolpath')
    return

def gcode_to_mbot(output_filename, text=None, filename=None, gcode_lines=None):
    if gcode_lines is None:
        if filename is not None:
            gcode_lines = open(filename).readlines()
        elif text is not None:
            gcode_lines = text.split("\n")
        else:
            raise ValueError("Too Few Parameters")

    toolpath_text, vardict = createToolpath(gcode_lines)
    metadata_text = generateMetajson(vardict)

    temp = tempfile.mkdtemp()
    with open('{}/meta.json'.format(temp), 'w') as metafile:
        metafile.write(metadata_text)
    with open('{}/print.jsontoolpath'.format(temp), 'w') as toolpathfile:
        toolpathfile.write(toolpath_text)
    
    packageMBotFile(output_filename, temp)
