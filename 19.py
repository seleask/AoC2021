import re

def read_scanner_beacons(s):
    return list(map(eval, s.split("\n")[:-2]))

def read_scanners(s):
    scanner_strings = re.compile("---\ scanner\ [0-9]+\ ---\n").split(s)[1:]
    return list(map(read_scanner_beacons, scanner_strings))

def manhattan_dist(a,b):
    return sum(map(lambda xy: abs(xy[0] - xy[1]), zip(a,b)))

# map set of distances to all other beacons to a beacon position
# in other words identify each beacon by the distances between it and all other beacons
def build_dist_map(beacons):
    m = {}

    for i, beacon in enumerate(beacons):
        distances = []
        for other_beacon in beacons[:i]+beacons[i+1:]:
            distances.append(manhattan_dist(beacon, other_beacon))

        m[frozenset(distances)] = beacon

    return m

dist_map_memo = {}
def build_dist_map_memo(beacons):
    beacons = tuple(beacons)
    if beacons in dist_map_memo:
        return dist_map_memo[beacons]
    else:
        result = build_dist_map(beacons)
        dist_map_memo[beacons] = result
        return result

# map points in map_a onto points in map_b
def overlap(map_a, map_b):
    matches = {}

    for dist_set_b in map_b.keys():
        for dist_set_a in map_a.keys():
            # I can't remember why exactly 10 as minimum but anything else breaks
            if len(dist_set_a.intersection(dist_set_b)) >= 10:
                matches[map_a[dist_set_a]] = map_b[dist_set_b]

    return matches

# return a mapping of overlapping beacons in a to beacons in b
# if they overlap
def are_overlapping(beacons_a, beacons_b):
    overlap_map = overlap(build_dist_map_memo(beacons_a), build_dist_map_memo(beacons_b))
    if len(overlap_map) >= 12:
        return overlap_map

def rotate_cw_in_y_once(coord):
    x,y,z = coord
    return (-z,y,x)

def rotate_cw_in_y(coord, times):
    if times == 0:
        return coord
    else:
        return rotate_cw_in_y(rotate_cw_in_y_once(coord), times-1)

def rotate_cw_in_z_once(coord):
    x,y,z = coord
    return (-y,x,z)

def rotate_cw_in_z(coord, times):
    if times == 0:
        return coord
    else:
        return rotate_cw_in_z(rotate_cw_in_z_once(coord), times-1)

def rotate_upwards(coord):
    x,y,z = coord
    return (x,-z,y)

def rotate_downwards(coord):
    x,y,z = coord
    return (x,z,-y)

front = lambda coord: coord
right = rotate_cw_in_y_once
back = lambda coord: rotate_cw_in_y(coord, 2)
left = lambda coord: rotate_cw_in_y(coord, 3)

up = rotate_upwards
down = rotate_downwards

def gen_orientations():
    orientation_fns = []
    orientations = [left, right, back, front, up, down]

    for orientation in orientations:
        for z_turns in range(0,4):
            orientation_fns.append(lambda coord, orientation=orientation, z_turns=z_turns: rotate_cw_in_z(orientation(coord), z_turns))

    return orientation_fns

all_orientations = gen_orientations()

# return the function that rotates coordinates (values) into the same orientation as the keys (coordinates), and the offset corresponding to the translation of values to keys (once rotated)
# in other words, offset is the position of scanner (values) once rotated to the same orientation as scanner (keys)
def find_orientation_by_mapping(overlap_map):
    def diff(a,b):
        return tuple(map(lambda xy: xy[0]-xy[1], zip(a,b)))

    for orientation_fn in all_orientations:
        diffs = list(map(lambda ab, orientation_fn=orientation_fn: diff(ab[0],orientation_fn(ab[1])), overlap_map.items()))
        if len(set(diffs)) == 1:
            return orientation_fn, diffs[0]

def find_overlapping_scanner(base_scanner, scanners):
    for scanner in scanners:
        overlap_map = are_overlapping(base_scanner["beacons"], scanner["beacons"])
        if overlap_map:
            print("overlap found between scanner ", base_scanner["id"], " and ",  scanner["id"])
            return overlap_map, scanner

def translate_beacons(orientation_fn, offset, beacons):
    def add(a,b):
        return tuple(map(lambda xy: xy[0]+xy[1], zip(a,b)))

    return list(map(lambda beacon: add(orientation_fn(beacon), offset), beacons))

def map_scanner_space(scanners):
    scanner_objs = []
    for i, scanner in enumerate(scanners):
        scanner_objs.append({"id": i, "beacons": scanner})

    scanners = scanner_objs
    base_scanner = scanners[0]
    scanners = scanners[1:]
    beacons = set(base_scanner["beacons"])
    scanner_positions = [(0,0,0)]

    while scanners:
        result = find_overlapping_scanner({"id": "super", "beacons": beacons}, scanners)
        if not result:
            print("search failed")
            print("no overlap found for super-scanner")
            print("remaining scanners: ", list(map(lambda s: s["id"], scanners)))
            return
        overlap_map, scanner = result
        orientation_fn, offset = find_orientation_by_mapping(overlap_map)
        translated_beacons = translate_beacons(orientation_fn, offset, scanner["beacons"])
        beacons = beacons.union(translated_beacons)
        scanner_positions.append(offset)

        scanners.remove(scanner)

    return beacons, scanner_positions

def solve_part_1(scanners):
    beacons, _ = map_scanner_space(scanners)
    return len(beacons)

def solve_part_2(scanners):
    _, scanner_positions = map_scanner_space(scanners)
    # reusing what I already had
    dist_map = build_dist_map(scanner_positions)
    max_distance = max(map(lambda distances: max(distances), dist_map.keys()))
    return max_distance
