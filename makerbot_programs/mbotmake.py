#!/usr/bin/env python3

import sys
import traceback

import makerbot_files

def main(argv):
    try:
        for gcode in argv[1:]:
            makerbot_files.gcode_to_mbot(gcode.replace(".gcode", ".makerbot"), filename=gcode)

    except Exception as e:
        print()
        print('An error occurred.')
        print('Please report this, as this may be a bug.')
        print('Go to https://github.com/sckunkle/mbotmake/issues and add a new issue.')
        # print('Also, add the contents of {} to a zip file and add it to the issue, if there is any.'.format(temp))
        traceback.print_exc()
        input()
        

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Instructions:')
        print('Drag and drop your generated gcode file onto this executable.')
        print('It will then output a makerbot file in the dir that the original gcode is placed in.')
        print('Press enter to continue.')
        input()
        sys.exit()
    main(sys.argv)
