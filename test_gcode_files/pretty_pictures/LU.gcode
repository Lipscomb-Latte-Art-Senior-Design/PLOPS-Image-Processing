; printable area is 100x100x100.
; first move to top at center (x,y,z)(0,0,6)
G1 X0 Y0 Z6 F5000
; set hotend temperature to 30°C (only bc the machine hates us)
M104 S180
; -------------------------------------------------------------------

; L
;G1 X-50 F1000 E40
G1 X-27 Y-21 F1000 E40
G1 X-27 Y22
G1 X-5 Y22

; U
G1 X4 Y-22 F1000 E70
G1 X4 Y16
G1 X6 Y19
G1 X11 Y22
G1 X20 Y22
G1 X24 Y20
G1 X27 Y15
G1 X27 Y-22

; -------------------------------------------------------------------
; End at top center
G1 X0 Y0 Z6 F100

M104 S0 ; turn off hot end

