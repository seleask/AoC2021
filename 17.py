import math

initial_pos = (0,0)

'''
Determine the peak of arc for a given y velocity
'''
def max_height_reached(yv):
    if yv < 0:
        return initial_pos[1]
    else:
        return (yv*(yv+1)) // 2

def value_in_range(v, rnge):
    lower, upper = rnge
    return lower <= v <= upper

'''
Determine whether a y velocity puts the probe in the target area for at least one step,
return the times/steps when this occurs
'''
def in_target_height_steps(yv, target_y_range):
    y_pos = initial_pos[1]
    target_lower,_ = target_y_range

    steps = 0
    in_target_steps = []

    while not (yv < 0 and y_pos < target_lower):
        if value_in_range(y_pos, target_y_range):
            in_target_steps.append(steps)

        y_pos += yv
        yv -= 1
        steps += 1
    return in_target_steps

'''
The maximum y velocity without overshooting target area after falling is distance between
y=0 and lower y bound of target area, inverted.
this follows from observation that launch velocity is inverted and increased by -1 when probe
falls back through y=0.
Probe always passes through zero as the upward arc is symmetrical, so if
velocity is greater than the distance from y=0 to the lower end of target area, it will
definitely overshoot it.
'''
def max_y_velocity(target_y_range):
    lower, upper = target_y_range
    target_length = upper-lower

    # (questionable) assume target area is below zero
    distance = 0-lower
    v = distance-1

    return v
'''
The lowest and highest possible x velocities are defined by
the target area. Use simplified quadratic equation to find the
velocity such that final x value of path is the lower x bound of the target area.
'''
def lower_and_upper_x_velocity(target_x_range):
    x_lower,x_upper = target_x_range

    def simplified_quadratic(x_bound):
        return (math.sqrt(1 + 8*x_bound) - 1) // 2

    lower = simplified_quadratic(x_lower)
    upper = x_upper
    return int(lower), upper

'''
Find x component after time t, just sum numbers up to velocity
unless velocity is greater than t, then use equation from Gauss
to compute sum of numbers between velocity and velocity-(t+1)
'''
def x_at_time(xv, t):
    if t >= xv:
        return (xv*(xv+1)) // 2
    else:
        t = t-1
        alpha = xv - t
        beta = xv
        l = (beta - alpha) + 1
        r = alpha + beta
        return (l*r) // 2
'''
Find any x velocities that cause path intersection for given y velocity
'''
def valid_xvs_for_yv(yv, target_x_range, target_y_range):
    ts = in_target_height_steps(yv, target_y_range)

    xv_lower, xv_upper = lower_and_upper_x_velocity(target_x_range)

    xvs = []
    for xv in range(xv_lower, xv_upper+1):
        for t in ts:
            x = x_at_time(xv, t)
            if value_in_range(x, target_x_range):
                xvs.append(xv)

    return set(xvs)

# part 1
def search(x_range, y_range):
    y_guess = max_y_velocity(y_range)
    for yv in range(y_guess+1)[::-1]:
        xv = valid_xv_for_yv(yv, x_range, y_range)
        if xv:
            return (xv[0], yv)

def min_y_velocity(y_range):
    y_lower, _ = y_range
    return y_lower


# part 2
def brute_force(x_range, y_range):
    initial_yv = max_y_velocity(y_range)

    vs = set()
    for yv in range(min_y_velocity(y_range), initial_yv+1)[::-1]:
        xvs = valid_xvs_for_yv(yv, x_range, y_range)
        vs = vs.union([(xv,yv) for xv in xvs])

    return vs


sample = '''23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7'''


example_vs = [(int(v[0]), int(v[1])) for v in map(lambda s: s.split(","), filter(lambda s: s != '', sample.replace("\n", " ").split(" ")))]

set(brute_force((20,30), (-10,-5))) == set(example_vs)
