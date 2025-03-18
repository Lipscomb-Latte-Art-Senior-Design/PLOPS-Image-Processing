; -------------------------- Start ------------------------------------
M104 S180; set hotend temperature

; Priming 200 mm
G1 X-40 Y30 F3000
G1 E-200 F600

; 4.5 mmE/mmT * 80 mmT = 360 mmE for total 560 mm so far
G1 X-40 Y15 F3000
G1 X40 E-560 F600
; 4.6 mmE/mmT * 80 mmT = 368 mmE for total 928 mm so far
G1 X-40 Y0 F3000
G1 X40 E-928 F600
; 4.7 mmE/mmT * 80 mmT = 376 mmE for total 1304 mm so far
G1 X-40 Y-15 F3000
G1 X40 E-1304 F600
; 4.8 mmE/mmT * 80 mmT = 384 mmE for total 1688 mm so far
G1 X-40 Y-30 F3000
G1 X40 E-1688 F600
; 4.9 mmE/mmT * 80 mmT = 392 mmE for total 2080 mm so far
G1 X-40 Y-45 F3000
G1 X40 E-2080 F600