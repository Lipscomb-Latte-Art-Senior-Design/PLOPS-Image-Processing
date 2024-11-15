; **************** PARAMETERS USED DURING CALCULATIONS ****************
; feedrate = 30 mm/s = 1800 mm/min      Speed of XY travel
; extrusion_per_mm = 0.7                Extrusion per amount of travel (mm/mm)
; step_angle = 10                       Angle in degrees between each point

; -------------------------- Start ------------------------------------
; first move to top at center (x,y,z)(0,0,6)
G1 X0 Y0 Z6 F5000
; set hotend temperature to 30°C (only bc the machine hates us)
M104 S180

; -------------------------- Circle ------------------------------------
; Outline of a 30mm radius full circle
; Center = (0, 0)
; Made of 36 equally spaced points
; Extrusion of 3.66mm per move(based on distance apart)

G1 X30.0000 Y0.0000 F1800
G1 X29.5442 Y5.2094 E-3.6605
G1 X28.1908 Y10.2606 E-7.3211
G1 X25.9808 Y15.0000 E-10.9816
G1 X22.9813 Y19.2836 E-14.6422
G1 X19.2836 Y22.9813 E-18.3027
G1 X15.0000 Y25.9808 E-21.9632
G1 X10.2606 Y28.1908 E-25.6238
G1 X5.2094 Y29.5442 E-29.2843
G1 X0.0000 Y30.0000 E-32.9449
G1 X-5.2094 Y29.5442 E-36.6054
G1 X-10.2606 Y28.1908 E-40.2660
G1 X-15.0000 Y25.9808 E-43.9265
G1 X-19.2836 Y22.9813 E-47.5870
G1 X-22.9813 Y19.2836 E-51.2476
G1 X-25.9808 Y15.0000 E-54.9081
G1 X-28.1908 Y10.2606 E-58.5687
G1 X-29.5442 Y5.2094 E-62.2292
G1 X-30.0000 Y0.0000 E-65.8897
G1 X-29.5442 Y-5.2094 E-69.5503
G1 X-28.1908 Y-10.2606 E-73.2108
G1 X-25.9808 Y-15.0000 E-76.8714
G1 X-22.9813 Y-19.2836 E-80.5319
G1 X-19.2836 Y-22.9813 E-84.1924
G1 X-15.0000 Y-25.9808 E-87.8530
G1 X-10.2606 Y-28.1908 E-91.5135
G1 X-5.2094 Y-29.5442 E-95.1741
G1 X-0.0000 Y-30.0000 E-98.8346
G1 X5.2094 Y-29.5442 E-102.4952
G1 X10.2606 Y-28.1908 E-106.1557
G1 X15.0000 Y-25.9808 E-109.8162
G1 X19.2836 Y-22.9813 E-113.4768
G1 X22.9813 Y-19.2836 E-117.1373
G1 X25.9808 Y-15.0000 E-120.7979
G1 X28.1908 Y-10.2606 E-124.4584
G1 X29.5442 Y-5.2094 E-128.1189


; ------------------------------ End ----------------------------------
; End at top center
G1 X0 Y0 Z6 F1000

M104 S0 ; turn off hot end
