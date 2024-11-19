; -------------------------- Start ------------------------------------
; first move to top at center (x,y,z)(0,0,6)
G1 X0 Y0 Z6 F5000
; set hotend temperature to 30°C (only bc the machine hates us)
M104 S180

G1 E500 F500

; ------------------------------ End ----------------------------------

M104 S0 ; turn off hot end