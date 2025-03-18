G28 % Auto Home
M83 % Set Extruder to Relative Mode
M107 % Turn off Vibrator

% Actual Center: (X: 55.0, Y: 59.0)
% "Printing" Center: (X: 58.0, Y: 59.0)
% We offset by 3mm in the X to account for the horizontal velocity of the
% powder coming out of the nozzle.

% === Move to Actual Center ===
% This is so the user can center the cup.
G1 X55.0 Y59.0 Z5.0 F10000
% G4 P1000 % Wait for move to finish
% M117 Place your cup.
% G4 P10000 % Wait 10000ms for user to place cup
M117 Printing...

% === Starting Position ===
G1 X58
G91
G1 X0.0 Y42.0
G90

% === Face Circle ===
G1 Z1.0
M106 S80 % Start Vibrator
G2 I0.0 J-42.0 E3.0 % Circle with extrusion
G2 I0.0 J-42.0 % Circle without extrusion
M107 % Stop Vibrator
G1 Z5.0 % Lift for Travel
G4 P50 % Wait 750ms before travel

% === Left Eye ===
G1 X38 Y45.0
G1 Z1.0
M106 S80 % Start Vibrator
G1 E0.1 % Drop the eye
G4 P400
M107 % Stop Vibrator
G1 Z5.0 % Lift for Travel

% End Shake
G4 P50 % Wait 750ms before travel

% === Right Eye ===
G1 X78 Y45.0
G1 Z1.0
M106 S80 % Start Vibrator
G1 E0.3 % Drop the eye
G4 P400
M107 % Stop Vibrator
G1 Z5.0 % Lift for Travel

% End Shake
G4 P50 % Wait 750ms before travel

% === Mouth ===
G1 X38 Y78.0
G1 Z1.0
M106 S80 % Start Vibrator
G2 X78 Y78 R30 E0.7
G3 X38 Y78 R30 E0.7
G2 X78 Y78 R30
M107 % Stop Vibrator
G1 Z5.0 % Lift for Travel

% End Shake
G4 P50 % Wait 750ms before travel

% === Presentation Position ===
G1 X0.0 Y107.0 Z110.0
M117 Enjoy 
