def read_lines(path):
    def process_line(s):
        points = s.strip().split(" -> ")
        point_pairs = list(map(lambda point: point.split(','), points))
        return list(map(lambda s: list(map(int, s)), point_pairs))
    lines = open(path).readlines()
    return list(map(process_line, lines))

def count_overlaps(lines):
    horizontal_lines = []
    vertical_lines = []
    diagonal_lines = []

    for line in lines:
        start,end = line
        x1,y1 = start
        x2,y2 = end

        if x1 == x2:
            vertical_lines.append(line)
        elif y1 == y2:
            horizontal_lines.append(line)
        else:
            diagonal_lines.append(line)

    points = {}
    total = 0

    def add_point(point):
        key = str(point)
        nonlocal points
        nonlocal total

        if points.get(key, 0) == 1:
            total += 1
            points[key] += 1
        elif points.get(key, 0) == 0:
            points[key] = 1

    def count_horizontal_or_vertical_lines(lines, varying_index):
        for line in lines:
            start,end = sorted([line[0][varying_index], line[1][varying_index]])
            static_index = varying_index^1

            point = [0,0]
            point[static_index] = line[0][static_index]

            for i in range(start, end+1):
                point[varying_index] = i
                add_point(point)


    def count_diagonal_line(line):
        start,end = line

        x_diff = end[0] - start[0]
        y_diff = end[1] - start[1]

        step_from_diff = lambda diff: -1 if diff < 0 else 1
        x_step, y_step = map(step_from_diff, [x_diff, y_diff])

        x = start[0]
        y = start[1]
        while x != end[0]+x_step and y != end[1]+y_step:
            point = [x,y]
            add_point(point)
            x += x_step
            y += y_step

    def count_diagonal_lines():
        for line in diagonal_lines:
            count_diagonal_line(line)

    count_horizontal_or_vertical_lines(horizontal_lines, 0)
    count_horizontal_or_vertical_lines(vertical_lines, 1)
    count_diagonal_lines()

    return total
