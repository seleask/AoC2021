import copy

left, right = 0,1

def regular_number(pair):
    l,r = pair
    return isinstance(l,int) and isinstance(r,int)

def is_pair(x):
    return isinstance(x, list) and len(x) == 2

def build_path(t, k):
    path = [t]
    node = t
    for selector in k:
        node = node[selector]
        path.append(node)

    return path

# build up a path to 4-levels-deep nested pair (exploding)
def find_explosion_candidate(t):
    def build_key(node, key=[]):
        if len(key) >= 4 and regular_number(node):
            return key

        l,r = node
        if is_pair(l):
            k = build_key(l, key+[left])
            if k:
                return k
        if is_pair(r):
            k = build_key(r, key+[right])
            if k:
                return k

    key = build_key(t)
    if key:
        return build_path(t, key)

"""
Derive a chain of selectors to a node in tree from a path (which is a list of
references to nodes ending in the node).
useful for reasoning about the path taken
through tree. Annoying to reason about that
from the path itself
"""
def key_from_path(path):
    key = []
    for parent, child in zip(path, path[1:]):
        selector = left if child is parent[left] else right
        key.append(selector)

    return key

def replace_exploded_pair_with_zero(parent, child):
    if child is parent[left]:
        parent[left] = 0
    else:
        parent[right] = 0


def add_to_lexicographically_next(path, side, amount):
    key = key_from_path(path)
    if all(selector == side for selector in key):
        return

    subtree = None
    for k, node in zip(reversed(key), list(reversed(path))[1:]):
        if not k == side:
            subtree = node
            break

    if not subtree:
        return

    if isinstance(subtree[side], int):
        subtree[side] += amount
        return

    node = subtree[side]
    opposite_side = side^1

    def walk_and_add(node):
        if isinstance(node[opposite_side], int):
            node[opposite_side] += amount
        else:
            walk_and_add(node[opposite_side])

    walk_and_add(node)

def add_to_lexicographically_left(path, amount):
    add_to_lexicographically_next(path, left, amount)

def add_to_lexicographically_right(path, amount):
    add_to_lexicographically_next(path, right, amount)


def explode(path):
    child = path[-1]
    parent = path[-2]

    lv, rv = child
    add_to_lexicographically_left(path, lv)
    add_to_lexicographically_right(path, rv)
    replace_exploded_pair_with_zero(parent, child)

def explode_leftmost_candidate(t):
    explosion_candidate = find_explosion_candidate(t)
    if explosion_candidate:
        explode(explosion_candidate)
        return True


def test_explode():
    t = [[[[[4,3],4],4],[7,[[8,4],9]]], [1,1]]
    exploded = explode_leftmost_candidate(t)
    assert(exploded)
    assert(t == [[[[0,7],4],[7,[[8,4],9]]],[1,1]])
    exploded = explode_leftmost_candidate(t)
    assert(exploded)
    assert(t == [[[[0,7],4],[15,[0,13]]],[1,1]])
    t = [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
    exploded = explode_leftmost_candidate(t)
    assert(exploded)
    assert(t == [[[[0,7],4],[[7,8],[6,0]]],[8,1]])


def test_debris():
    t_original = [[[[[4,3],4],4],[7,[[8,4],9]]], [1,1]]

    t = copy.deepcopy(t_original)
    parent = t[0][0][0]
    child = parent[0]
    path = [t, t[0], t[0][0], parent, child]

    add_to_lexicographically_left(path, 10)
    assert(t == t_original)

    add_to_lexicographically_right(path, 10)
    assert(t == [[[[[4,3],14],4],[7,[[8,4],9]]], [1,1]])

    t = [[4,3],[[[1,2],3],4]]
    path = [t, t[0]]

    add_to_lexicographically_right(path, 10)
    assert(t == [[4,3],[[[11,2],3],4]])


def is_splittable(node):
    return isinstance(node, int) and node >= 10

def find_split_candidate(t):
    def build_key(node, key=[]):
        if is_splittable(node):
            return key

        if not is_pair(node):
            return

        l,r = node
        k = build_key(l, key+[left])
        if k:
            return k

        k = build_key(r, key+[right])
        if k:
            return k

    key = build_key(t)
    if key:
       return build_path(t, key)

def split(path):
    split_item = path[-1]
    enclosing_pair = path[-2]

    assert(isinstance(split_item, int) and split_item >= 10)
    lhs = split_item // 2
    rhs = lhs if split_item % 2 == 0 else lhs+1

    selector = left if split_item is enclosing_pair[left] else right

    enclosing_pair[selector] = [lhs, rhs]

def split_leftmost_candidate(t):
    path = find_split_candidate(t)

    if path:
        split(path)
        return True

def test_split():
    t = [[[20,1],2],3]
    split_leftmost_candidate(t)
    assert(t == [[[[10, 10], 1], 2], 3])

    t = [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
    split_leftmost_candidate(t)
    assert(t == [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]])

def execute_to_quiescence(f):
    def fn(tree):
        result = True
        executed_at_least_once = False
        while result:
            result = f(tree)
            if result:
                executed_at_least_once = True

        return executed_at_least_once

    return fn

reduce_to_quiescence = execute_to_quiescence(lambda t: explode_leftmost_candidate(t) \
                                             or split_leftmost_candidate(t))

def test_reduction():
    t = [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
    reduce_to_quiescence(t)
    assert(t == [[[[0,7],4],[[7,8],[6,0]]],[8,1]])


sample_homework = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
"""

def read_homework(s):
    return list(map(eval, s.split('\n')[:-1]))

def reduce_homework(snailfish_nums):
    num = snailfish_nums[0]
    reduce_to_quiescence(num)

    for next_num in snailfish_nums[1:]:
        num = [num, next_num]
        reduce_to_quiescence(num)

    return num

def test_reduction():
    t = [[[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]], [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]]
    reduce_to_quiescence(t)
    assert(t == [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]])

    hw = read_homework(sample_homework)
    num = reduce_homework(hw)
    assert(num == [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])

## Part1
def calculate_magnitude(num):
    if not is_pair(num):
        return num

    l,r = num
    return calculate_magnitude(l)*3 + calculate_magnitude(r)*2


## Part 2
def generate_sum_pairs(nums):
    pairs = []
    for i in range(len(nums)):
        for j in range(i+1,len(nums)):
            pairs.append([nums[i], nums[j]])
            pairs.append([nums[j], nums[i]])

    return pairs


def find_largest_sum(num_pairs):
    best_mag = 0

    for num_sum in num_pairs:
        s = copy.deepcopy(num_sum)
        reduce_to_quiescence(s)
        mag = calculate_magnitude(s)
        best_mag = max(best_mag, mag)

    return best_mag
