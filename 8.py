from collections import defaultdict

def read_patterns(f):
    lines = open(f, 'r').readlines()


    pattern_number_pairs = []
    for line in lines:
        patterns,number = line.split("|")
        pattern_list = patterns.strip().split(' ')
        digits_list = number.strip().split(' ')
        assert len(pattern_list) == 10
        assert len(digits_list) == 4
        pattern_number_pairs.append([pattern_list, digits_list])

    return pattern_number_pairs


### Part I ###

def count_simples(patterns_digits_pair):
    digits = patterns_digits_pair[1]

    total = 0
    for digit in digits:
        if len(digit) in [2, 4, 3, 7]:
            total += 1

    return total


### Part II ###

def map_pattern_lengths(patterns):
    patterns_by_length = defaultdict(list)
    for pattern in patterns:
        length = len(pattern)
        patterns_by_length[length] += ["".join(sorted(pattern))]

    return patterns_by_length


def deduce_mapping(patterns):
    patterns_by_length = map_pattern_lengths(patterns)
    numbers = {}

    # populate with the simple cases
    for n, length in {1:2, 4:4, 7:3, 8:7}.items():
        numbers[n] = patterns_by_length[length][0]

    six_segment_patterns = patterns_by_length[6]

    # subtract 4 from 8 to get the "aeg" segments
    aeg = set(numbers[8]).difference(numbers[4])

    # 9 is the only six segment number that doesn't contain all of a,e,g.
    for pattern in six_segment_patterns:
        if not all(c in pattern for c in aeg):
            numbers[9] = pattern
            break
    assert numbers[9]

    six_segment_patterns.remove(numbers[9])

    # 0 contains 7, 6 doesn't.
    for pattern in six_segment_patterns:
        if all(c in pattern for c in numbers[7]):
            numbers[0] = pattern
        else:
            numbers[6] = pattern

    assert numbers[0]
    assert numbers[6]

    # 5 is 6 with a segment missing
    five_segment_patterns = patterns_by_length[5]
    for pattern in five_segment_patterns:
        if all(c in numbers[6] for c in pattern):
            numbers[5] = pattern
            break

    assert numbers[5]

    five_segment_patterns.remove(numbers[5])

    # 3 is distinguished from 2 by containing 1
    p1, p2 = five_segment_patterns
    diff = list(set(p1).difference(p2)) + list(set(p2).difference(p1))
    numbers[3], numbers[2] = [p1, p2] if all(c in p1 for c in numbers[1]) else [p2, p1]

    return numbers


def identify_digits(mapping, digits):
    number_s = ""

    for digit in digits:
       number_s += str(mapping["".join(sorted(digit))])

    return int(number_s)


def solve(patterns_digits_pairs):
    total = 0
    for patterns, digits in patterns_digits_pairs:
        mapping = deduce_mapping(patterns)
        # invert the mapping from number->pattern to pattern->number
        inverted_mapping = {"".join(sorted(v)):k for k,v in mapping.items()}
        total += identify_digits(inverted_mapping, digits)

    return total
