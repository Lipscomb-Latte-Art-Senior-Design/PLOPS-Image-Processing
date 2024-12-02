
import math


def generate_circular_arc_vertices(center=(0, 0), radius=1, arc=(0, 360), angular_resolution=10):
    points = []      # Initialize list of vertices

    # Reverse direction if arc direction is reversed.
    # This will default (with 0 -> 360) to CCW, but CW can be achieved with 360 -> 0.
    if arc[1] < arc[0]:
        angular_resolution *= -1

    # Loop through angles in the Arc tuple with a step size of angular_resolution
    # See https://docs.python.org/3/library/functions.html#func-range
    for a in range(arc[0], arc[1], angular_resolution):
        angle = math.radians(a) # convert to radians for trig calcs
        
        # (Rcos(θ) + X_offset, Rsin(θ) + Y_offset)
        points.append( (math.cos(angle) * radius + center[0], math.sin(angle) * radius + center[1]) )
    
    return points

## By Gracelyn: generates points and puts them into the command list structure
def generate_arc(center=(0, 0), radius=1, arc=(0, 360), angular_resolution=10, extrusion_per_mm=4.5, cummulative_extrusion=0):
    # Calculating just the coordinates
    points = generate_circular_arc_vertices(center=center, radius=radius, arc=arc, angular_resolution=angular_resolution)    
    

    # Putting the coordinates into the command list format
    arc_commands = []

    for i, point in enumerate(points):
        if i == 0:
            arc_commands.append((*point, None, None, travel_vel))
            continue # end this iteration of the for loop
        
        # Dist from last point to this point
        dist = math.sqrt((point[0] - points[i-1][0])**2 + (point[1] - points[i-1][1])**2)

        time_taken = dist / draw_vel
        extrude_dist = extrusion_per_mm * dist
        extruder_speed = extrude_dist / time_taken
        # is that not just extruder speed = extrude / draw_vel

        modified_draw_vel = math.sqrt(draw_vel**2 + extruder_speed**2) # Specific to Makerbot

        cummulative_extrusion += extrude_dist  # Value for extrusion command

        arc_commands.append((*point, None, extrude_dist, modified_draw_vel))

    return arc_commands

# My command structure is Tuple (ABS X, ABS Y, ABS Z, REL E, VEL Travel) w/ None used for not specified
# VEL is in mm/s. extrude is in mmE/mmT

def generate_line(start=(0, 0, None), end=(0, 0, None), extrude=0, travel_vel=0, draw_vel=0, include_start=True):
    dist = math.sqrt(
        ((end[0]-start[0])**2 if start[0] is not None and end[0] is not None else 0) +
        ((end[1]-start[1])**2 if start[1] is not None and end[1] is not None else 0) +
        ((end[2]-start[2])**2 if start[2] is not None and end[2] is not None else 0))

    time_taken = dist / draw_vel
    extrude_dist = extrude * dist
    extruder_speed = extrude_dist / time_taken

    modified_draw_vel = math.sqrt(draw_vel**2 + extruder_speed**2) # Specific to Makerbot

    commands = []
    if include_start: commands.append((*start, None, travel_vel))
    commands.append((*end, extrude_dist, modified_draw_vel))

    return commands

def generate_lines_through_2d_points(points=[], extrude=0, travel_vel=0, draw_vel=0):
    commands = []
    
    for i, point in enumerate(points):
        if i == 0:
            commands.append((*point, None, 0, travel_vel))

            continue # end this iteration of the for loop

        commands += generate_line(start=(*points[i - 1], None), end=(*points[i], None), extrude=extrude, travel_vel=travel_vel, draw_vel=draw_vel, include_start=False)
    
    return commands

def generate_priming(priming_location=(0,0,0), prime_dist=200, travel_vel=0, draw_vel=0):
    commands = []
    commands.append((*priming_location, None, travel_vel))
    commands.append((None, None, None, prime_dist, draw_vel))
    return commands

def commands_to_gcode(commands, negative_extruder=True):
    gcode_lines = []

    total_extrusion = 0

    for i, command in enumerate(commands):
        if command[3] is not None:
            if negative_extruder:
                total_extrusion -= command[3]
            else:
                total_extrusion += command[3]
        
        X = ("X%.2f" % command[0]) if command[0] is not None else ""
        Y = ("Y%.2f" % command[1]) if command[1] is not None else ""
        Z = ("Z%.2f" % command[2]) if command[2] is not None else ""
        E = ("E%.2f" % total_extrusion) if command[3] is not None else ""
        F = ("F%.2f" % (command[4] * 60))

        gcode_lines.append("G1 " + " ".join([X, Y, Z, E, F]))
    
    return gcode_lines

travel_vel = 80
draw_vel = 10

###### Example generate full program
# prime_commands = generate_priming((-40, 30, 6), travel_vel=travel_vel, draw_vel=draw_vel)

# points = generate_circular_arc_vertices(center=(0, 0), radius=30, arc=(0, 360), angular_resolution=10)
# circle_commands = generate_lines_through_2d_points(points=points, extrude=5, travel_vel=travel_vel, draw_vel=draw_vel)

# commands = prime_commands + circle_commands

# gcode_lines = commands_to_gcode(commands=commands)

# print("\n".join(gcode_lines))