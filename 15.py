from queue import PriorityQueue

def read_risk_matrix(f):
    rows = open(f).read().split('\n')[:-1]
    return list(map(lambda row: list(map(int, row)), rows))

def neighbours(width, height, position):
    x,y = position

    neighbours = list(filter(lambda point: 0 <= point[0] < height \
                             and 0 <= point[1] < width, \
                             [(x+1,y),
                              (x-1,y),
                              (x,y+1),
                              (x,y-1)]))

    return neighbours

def lookup_with_scaling(width, height, matrix, i, j):
    downscaled_i = i % height
    downscaled_j = j % width

    risk = matrix[downscaled_i][downscaled_j]
    scaling_factor = (i // height) + (j // width)

    scaled_risk = risk + scaling_factor
    return scaled_risk if scaled_risk < 10 else (scaled_risk + 1) % 10

def search(matrix, scaling_factor=1):
    height = len(matrix)
    width = len(matrix[0])
    scaled_height = height*scaling_factor
    scaled_width = width*scaling_factor

    initial_pos = (0,0)
    goal_pos = (scaled_width-1, scaled_height-1)

    lowest_risk_to_pos = {initial_pos: 0}
    visited = set(initial_pos)

    pq = PriorityQueue()
    pq.put((0, initial_pos))

    while not pq.empty():
        (risk, current_pos) = pq.get()
        visited.add(current_pos)

        for neighbour in neighbours(scaled_width, scaled_height, current_pos):
            i,j = neighbour
            neighbour_risk = lookup_with_scaling(width, height, matrix, i, j)
            if neighbour not in visited:
                old_lowest_risk = lowest_risk_to_pos.get(neighbour, float('inf'))
                new_lowest_risk = lowest_risk_to_pos.get(current_pos, float('inf')) + neighbour_risk
                if new_lowest_risk < old_lowest_risk:
                    pq.put((new_lowest_risk, neighbour))
                    lowest_risk_to_pos[neighbour] = new_lowest_risk


    return lowest_risk_to_pos[goal_pos]

def print_matrix(m, scaling_factor=1):
    width = len(m[0])
    height = len(m)

    for i in range(height*scaling_factor):
        for j in range(width*scaling_factor):
            print(lookup_with_scaling(width, height, m, i, j), end="")

        print()
