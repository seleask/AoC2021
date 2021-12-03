

def dive(arr):

    depth = 0
    distance = 0

    for s in arr:
        op, value_s = s.split(' ')
        value = int(value_s)

        if op == "forward":
            distance += value
        elif op == "down":
            depth += value
        else:
            depth -= value

    return depth*distance


# down and up increase/decrease aim.
# forward increases horizontal position by X, but depth is increased by aim*X.
def dive_aim(arr):

    depth = 0
    distance = 0
    aim = 0

    for s in arr:
        op, value_s = s.split(' ')
        value = int(value_s)

        if op == "down":
            aim += value
        elif op == "up":
            aim -= value
        else:
            distance += value
            depth += aim*value

    return depth*distance

