grid_width = 10


def cell_neighbours(i,j):
    neighbours = []

    for a in range(-1, 2):
        for b in range(-1, 2):
            x = i+a
            y = j+b

            if a == b == 0:
                continue

            if 0 <= x < grid_width and 0 <= y < grid_width:
                neighbours.append((i+a, j+b))

    return neighbours


def simulate_step(grid):
    flash_count = 0

    neighbours = [(i,j) for i in range(grid_width) for j in range(grid_width)]
    flashed = set()

    while neighbours:
        i,j = neighbours[-1]
        neighbours.pop()

        if (i,j) in flashed:
            continue

        grid[i][j] += 1
        level = grid[i][j]

        if level > 9:
            grid[i][j] = 0
            flashed.add((i,j))
            neighbours += cell_neighbours(i,j)
            flash_count += 1

    return flash_count, grid


def simulate_steps(n, grid):
    flash_count = 0

    for _ in range(n):
        fc, grid = simulate_step(grid)
        flash_count += fc

    return flash_count


def grid_is_synchronised(grid):
    return all(all(level == 0 for level in row) for row in grid)


def find_first_synch(grid):
    step = 0
    while not grid_is_synchronised(grid):
        _, grid = simulate_step(grid)
        step += 1

    return step
