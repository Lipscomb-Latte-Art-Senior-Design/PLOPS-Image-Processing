
from geometry_funcs import generate_priming, generate_arc, commands_to_gcode

travel_vel = 80  # s/mm
draw_vel = 10  # s/mm
primeDist = 200  # mm

####### Smiley Face Parameters #######
left_eye = (-7, 20)  # (x,y)
right_eye = (8, 20)  # (x,y)
smile_center = (1, 11)  # (x,y)
circle_center = (1, 11)  # (x,y)

smile_radius = 15  # mm
circle_radius = 30  # mm

smile_arc = (206, 334) # start and stop are both 26 degrees below the horizontal
#######################################

# commands: (X, Y, Z, E command, F command)
commands = []
# generate priming routine
commands += generate_priming((-40, 30, 6), prime_dist=primeDist, travel_vel=travel_vel, draw_vel=draw_vel)
cummulative_extrusion = commands[len(commands)-1][3]  # this is the correct way to access the last extrusion value in the list

# generate complete circle for smiley face border
commands += generate_arc(center=circle_center, radius=circle_radius, arc=(0, 360), angular_resolution=10, extrusion_per_mm=4.5, cummulative_extrusion=cummulative_extrusion)
cummulative_extrusion = commands[len(commands)-1][3]

# generate arc for smile
commands += generate_arc(center=smile_center, radius=smile_radius, arc=smile_arc, angular_resolution=10, extrusion_per_mm=4.5, cummulative_extrusion=cummulative_extrusion)
cummulative_extrusion = commands[len(commands)-1][3]

# left eye -- using the priming function but on smaller scale to make the dots for the eyes
commands += generate_priming((*left_eye, None), prime_dist=8, travel_vel=travel_vel, draw_vel=draw_vel)
cummulative_extrusion = commands[len(commands)-1][3]

# right eye -- using the priming function but on smaller scale to make the dots for the eyes
commands += generate_priming((*right_eye, None), prime_dist=8, travel_vel=travel_vel, draw_vel=draw_vel)
cummulative_extrusion = commands[len(commands)-1][3]

# Convert to gcode command text
gcode_lines = commands_to_gcode(commands=commands, negative_extruder=False)

print("\n".join(gcode_lines))


