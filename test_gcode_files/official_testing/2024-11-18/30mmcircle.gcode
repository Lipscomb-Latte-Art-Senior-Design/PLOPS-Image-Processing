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

G1 X30.0000 Y0.0000
G1 X29.5442 Y5.2094 E-153.6605
G1 X28.1908 Y10.2606 E-157.3211
G1 X25.9808 Y15.0000 E-160.9816
G1 X22.9813 Y19.2836 E-164.6422
G1 X19.2836 Y22.9813 E-168.3027
G1 X15.0000 Y25.9808 E-171.9632
G1 X10.2606 Y28.1908 E-175.6238
G1 X5.2094 Y29.5442 E-179.2843
G1 X0.0000 Y30.0000 E-182.9449
G1 X-5.2094 Y29.5442 E-186.6054
G1 X-10.2606 Y28.1908 E-190.2660
G1 X-15.0000 Y25.9808 E-193.9265
G1 X-19.2836 Y22.9813 E-197.5870
G1 X-22.9813 Y19.2836 E-201.2476
G1 X-25.9808 Y15.0000 E-204.9081
G1 X-28.1908 Y10.2606 E-208.5687
G1 X-29.5442 Y5.2094 E-212.2292
G1 X-30.0000 Y0.0000 E-215.8897
G1 X-29.5442 Y-5.2094 E-219.5503
G1 X-28.1908 Y-10.2606 E-223.2108
G1 X-25.9808 Y-15.0000 E-226.8714
G1 X-22.9813 Y-19.2836 E-230.5319
G1 X-19.2836 Y-22.9813 E-234.1924
G1 X-15.0000 Y-25.9808 E-237.8530
G1 X-10.2606 Y-28.1908 E-241.5135
G1 X-5.2094 Y-29.5442 E-245.1741
G1 X-0.0000 Y-30.0000 E-248.8346
G1 X5.2094 Y-29.5442 E-252.4952
G1 X10.2606 Y-28.1908 E-256.1557
G1 X15.0000 Y-25.9808 E-259.8162
G1 X19.2836 Y-22.9813 E-263.4768
G1 X22.9813 Y-19.2836 E-267.1373
G1 X25.9808 Y-15.0000 E-270.7979
G1 X28.1908 Y-10.2606 E-274.4584
G1 X29.5442 Y-5.2094 E-278.1189


; ------------------------------ End ----------------------------------
; End at top center
G1 X0 Y0 Z6 F1000

M104 S0 ; turn off hot end
