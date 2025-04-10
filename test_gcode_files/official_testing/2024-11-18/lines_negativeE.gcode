; -------------------------- Start ------------------------------------
; first move to top at center (x,y,z)(0,0,6)
G1 X-40 Y-40 Z6 F5000
; set hotend temperature 
M104 S180

; ---------------------------------------------------------------------
; -40 to 40 in 

; ------------------- Prime -------------------------------------------
; prime in left corner
G1 E-200 F500

; -------------------- Lines -------------------------------------------
; top line
G1 X-40 Y-20 F3000
G1 X40 E-240 F300

; line 2
G1 X-40 Y-5 F3000
G1 X40 E-288 F300

; line 3
G1 X-40 Y10 F3000
G1 X40 E-344 F300

; line 3
G1 X-40 Y25 F3000
G1 X40 E-408 F300

; line 4
G1 X-40 Y40 F3000
G1 X40 E-480 F300

; ------------------ End -------------------------------------------------
M104 S0 ; turn off hot end