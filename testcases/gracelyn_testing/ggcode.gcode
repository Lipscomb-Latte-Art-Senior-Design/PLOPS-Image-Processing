; printable area is 100x100x100.
; first move to top at center (x,y,z)(0,0,6)
G1 X0 Y0 Z6 F5000
; set hotend temperature to 30°C (only bc the machine hates us)
M104 S180

; Move full X travel
G1 X-50 F1000 E40
G1 X50
G1 X0

; End at top center
G1 X0 Y0 Z6 F100

M104 S0 ; turn off hot end
