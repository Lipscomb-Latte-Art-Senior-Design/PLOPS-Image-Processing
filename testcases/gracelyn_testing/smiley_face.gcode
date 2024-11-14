; printable area is 100x100x100.
; first move to top at center (x,y,z)(0,0,6)
G1 X0 Y0 Z6 F5000
; set hotend temperature to 30°C (only bc the machine hates us)
M104 S180
; -------------------------------------------------------------------

; Circle for the smiley face
G1 X-34 Y-6 F1000 E40   ; I have no clue how long the extruder will spin for
G1 X-31 Y-16
G1 X-26 Y-22
G1 X-15 Y-31
G1 X-8 Y-33
G1 X-3 Y-34
G1 X4 Y-34
G1 X8 Y-33
G1 X14 Y-31
G1 X21 Y-27
G1 X27 Y-21
G1 X30 Y-16
G1 X32 Y-13
G1 X34 Y-3
G1 X34 Y4
G1 X32 Y11
G1 X30 Y17
G1 X21 Y27
G1 X14 Y31
G1 X8 Y3
G1 X3 Y34
G1 X-3 Y34
G1 X-12 Y32
G1 X-21 Y27
G1 X-27 Y21
G1 X-31 Y14
G1 X-33 Y8
G1 X-34 Y2
G1 X-34 Y-6

; Right eye
G1 X13 Y-24

; Left eye
G1 X-13 Y-14

; Mouth (left to right)
G1 X-17 Y10
G1 X-14 Y14
G1 X-9 Y17
G1 X-3 Y19
G1 X3 Y19
G1 X9 Y17
G1 X13 Y14
G1 X15 Y13
G1 X17 Y10


; -------------------------------------------------------------------
; End at top center
G1 X0 Y0 Z6 F100

M104 S0 ; turn off hot end

