; -------------------------- Start ------------------------------------
M104 S180; set hotend temperature 

; Priming 200 mm ------------------------------------------------------
G1 X-40 Y30 F3000
G1 E-200 F300

; 1.0 mmE/mmT * 80 mmT = 80 mmE for total 280 mm so far
G1 X-40 Y15 F3000
G1 X40 E-280 F300
; 1.1 mmE/mmT * 80 mmT = 88 mmE for total 368 mm so far
G1 X-40 Y0 F3000
G1 X40 E-368 F300
; 1.2 mmE/mmT * 80 mmT = 96 mmE for total 464 mm so far
G1 X-40 Y-15 F3000
G1 X40 E-464 F300
; 1.3 mmE/mmT * 80 mmT = 104 mmE for total 568 mm so far
G1 X-40 Y-30 F3000
G1 X40 E-568 F300
; 1.4 mmE/mmT * 80 mmT = 112 mmE for total 680 mm so far
G1 X-40 Y-45 F3000
G1 X40 E-680 F300