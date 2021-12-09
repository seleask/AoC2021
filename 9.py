### Part I ###

def adjacent_coords(point, i_bound, j_bound):
    i,j = point
    left = [i, j-1]
    right = [i, j+1]
    up = [i-1, j]
    down = [i+1, j]

    return list(filter(lambda coord: 0 <= coord[0] < i_bound \
                           and 0 <= coord[1] < j_bound, \
                       [left, right, up, down]))


def find_low_points(height_map):
    low_points = []

    for i in range(len(height_map)):
        for j in range(len(height_map[0])):
            height_value = height_map[i][j]
            if all(height_map[a][b] > height_value \
                   for a,b in adjacent_coords([i,j], len(height_map), len(height_map[0]))):
                low_points.append([i,j])

    return low_points


def sum_risk_levels(height_map):
    low_points = find_low_points(height_map)
    return sum(map(lambda v: height_map[v[0]][v[1]]+1, low_points))


### Part II ###

def expand_basin(height_map, low_point):
    i_bound = len(height_map)
    j_bound = len(height_map[0])

    basin = []
    stack = [low_point]

    while stack:
        point = stack.pop()
        i,j = point

        if not(point in basin or height_map[i][j] == 9):
            basin.append(point)
            neighbours = adjacent_coords(point, i_bound, j_bound)
            stack += neighbours

    return basin


def expand_basins(height_map):
    low_points = find_low_points(height_map)

    basin_sizes = []
    for low_point in low_points:
        basin_sizes.append(len(expand_basin(height_map, low_point)))

    total = 1
    for size in sorted(basin_sizes)[-3:]:
        total *= size

    return total
