; This is a very simple gcode file that tests some of the basic functions
; we need the makerbot to do. It moves at a few different speeds, sets the
; hot end and bed to low temps [another test can see if it can run with them
; off]. We will see if it homes the axes before / after printing.

; printable area is 100x100x100.
; first move to top at center (x,y,z)(0,0,100)
G1 X0 Y0 Z100 F5000
; set hotend temperature to 30Â°C (only bc the machine hates us)
M104 S180

; ; Need to indicate to the user that we are ready for the cup to be placed.
; ; Move full X travel
; G1 X-50 F1000
; G1 X50
; G1 X0
; ; Move full Y travel
; G1 Y-50
; G1 Y50
; G1 Y0

; Begin printing image
; This is just a few concentric squares.

; Move to cup level, I guess
G1 Z20
G1 E-15 F5000

; First circle, r=10mm =======
; move to start, we're moving clockwise
G1 X10 Y0 F1000

G1 X10  Y10 E-30
G1 X-10 Y10 E-45
G1 X-10 Y-10 E-60
G1 X10  Y-10 E-75
G1 X10  Y0 E-90

; Second circle, r=20mm =======
; move to start, we're moving clockwise
G1 X20 Y0

G1 X20  Y10 E-105
G1 X-20 Y10 E-120
G1 X-20 Y-20 E-135
G1 X20  Y-20 E-150
G1 X20  Y0 E-165

; Third circle, r=30mm =======
; move to start, we're moving clockwise
G3 X30 Y0

G3 X30  Y30 E-180
G3 X-30 Y30 E-195
G3 X-30 Y-30 E-210
G3 X30  Y-30 E-225
G3 X30  Y0 E-240

; End printing image

; End at top center
G1 X0 Y0 Z100.0 F1000

M104 S0 ; turn off hot end