from operator import itemgetter

def parse_dot(dot_str):
    x,y = dot_str.split(',')
    return (int(x), int(y))

fold_chars_discard = "fold along "

def parse_fold_instruction(instruct_str):
    fold_str = instruct_str[len(fold_chars_discard):]
    direction, pos = fold_str.split('=')
    return (direction, int(pos))

def read_transparent_paper(f):
    dot_string, instruct_string = open(f).read().split("\n\n")

    dot_strings = dot_string.split('\n')
    dots = list(map(parse_dot, dot_strings))

    instruct_strings = instruct_string.split('\n')[:-1]
    fold_instructions = list(map(parse_fold_instruction, instruct_strings))

    return set(dots), fold_instructions

def dot_is_inside_of_fold(fold_direction, fold_position, dot):
    dot_x, dot_y = dot
    if fold_direction == 'x':
        return dot_x < fold_position
    else:
        return dot_y < fold_position

def mirror_dot(fold_direction, fold_position, dot):
    dot_mut = list(dot)

    mirrored_index = 0 if fold_direction == 'x' else 1
    diff = dot_mut[mirrored_index] - fold_position
    dot_mut[mirrored_index] = fold_position - diff

    dot_x, dot_y = dot_mut
    dot = (dot_x, dot_y)
    return dot

## Part 1

def count_dots_after_fold(dot_positions, fold_direction, fold_position):
    dots = 0

    for dot in dot_positions:
        if dot_is_inside_of_fold(fold_direction, fold_position, dot):
            dots += 1
        else:
            dot = mirror_dot(fold_direction, fold_position, dot)

            if not dot in dot_positions:
                dots += 1

    return dots


def count_dots_after_first_fold(dots, folds):
    fold_direction, fold_position = folds[0]
    return count_dots_after_fold(dots, fold_direction, fold_position)

## Part 2

def fold_paper(dots, fold_direction, fold_position):
    folded_dots = set()
    for dot in dots:
        if not dot_is_inside_of_fold(fold_direction, fold_position, dot):
            mirrored_dot = mirror_dot(fold_direction, fold_position, dot)
            if not mirrored_dot in dots:
                folded_dots.add(mirrored_dot)

        else:
            folded_dots.add(dot)

    return folded_dots

def fold_completely(dots, fold_instructions):
    for fold_direction, fold_position in fold_instructions:
        dots = fold_paper(dots, fold_direction, fold_position)

    return dots

def print_paper(dots):
    # not very efficient, but simpler than sorting and iterating through
    # dots intermingled with printing/padding with '.'
    columns = max(map(itemgetter(0), dots))+1
    rows = max(map(itemgetter(1), dots))+1

    grid = [['.']*columns for _ in range(rows)]

    for x,y in dots:
        grid[y][x] = '#'

    for row in grid:
        print("".join(row))
