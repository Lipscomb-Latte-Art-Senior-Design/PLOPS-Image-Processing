
from geometry_funcs import generate_priming, generate_line, commands_to_gcode

# totalE = 0
# lineLength = 80

travel_vel = 80
draw_vel = 10
primeDist = 200

# travelSpeed = 3000
# lineSpeed = 600

# # Priming
# print("; Priming %.0f mm" % primeDist)
# print("G1 X-40 Y30 F%.0f" % travelSpeed)
# print("G1 E-%.0f F%.0f" % (primeDist, lineSpeed))
# totalE += primeDist
# print()

# for y, e in zip(range(15, -50, -15), range(45, 50, 1)):
#     e /= 10
#     totalE += e * lineLength
#     # (-40, -20) -> (40, -20), e mmE/mmT, +e*lineSpeed, 240, R: 
#     print("; %.1f mmE/mmT * %.0f mmT = %.0f mmE for total %.0f mm so far" % (e, lineLength, e * lineLength, totalE))
#     print("G1 X-40 Y%.0f F%.0f" % (y, travelSpeed))
#     print("G1 X40 E-%.0f F%.0f" % (totalE, lineSpeed))

#     # print("(-40, %.0f) -> (40, %.0f), %.1f mmE/mmT, +%.0f, %.0f, R: " % (y, y, e, e * lineLength, totalE))

commands = []
commands += generate_priming((-40, 30, 6), travel_vel=travel_vel, draw_vel=draw_vel, prime_dist=primeDist)

for y, e in zip(range(15, -50, -15), range(5, 10, 1)):
    e /= 10
    commands += generate_line(start=(-40, y, None), end=(40, y, None), extrude=e, travel_vel=travel_vel, draw_vel=draw_vel, include_start=True)


gcode_lines = commands_to_gcode(commands=commands, negative_extruder=False)

print("\n".join(gcode_lines))