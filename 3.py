

# gamma is the sum of powers of two corresponding to positions where most common bit is 1
def gamma(bitstrings,bitstring_length):
    result = 0
    bit_value = 1
    for i in range(bitstring_length):
        count = 0
        for j in range(len(bitstrings)):
            if bitstrings[j][bitstring_length-1-i] == '1':
                count += 1
            else:
                count -= 1

        if count > 0:
            result += bit_value

        bit_value *= 2

    return result

# epsilon is ~gamma
epsilon_from_gamma = lambda g, bitstring_length: (1 << bitstring_length) - 1 - g

# P = gamma*epsilon
def power(bitstrings):
    bitstring_length = len(bitstrings[0])
    g = gamma(bitstrings, bitstring_length)
    e = epsilon_from_gamma(g, bitstring_length)

    return g*e


### Part II ###

# life support rating = oxygen generator rating * co2 scrubber rating
# Use a trie to efficiently get the subset of bitstrings that match. Trie is binary and ratings are fixed length, which simplifies things. Storing the number of children in each node allows to easily identify when to short-circuit the search and straightforward to determine the most/least common next bit.

def prefix_tree(strings):
    leaf_depth = len(strings[0])
    tree = []

    for s in strings:
        node = tree
        for i in range(leaf_depth):
            if not node:
                node += [[],[],0]

            if s[i] == '0':
                node[2] += 1
                node = node[0]
            else:
                node[2] += 1
                node = node[1]

        node.append(s)

    return tree


# when there's one leaf beneath a node, find it and return its value.
def find_only_leaf(node):
    while len(node) == 3:
        node = node[0] or node[1]

    return node[0]


def find_rating(tree, preferred_bit):
    node = tree

    # when there are two child nodes, we can decide between them.
    # if there's one child node, we are done.
    while node[2] > 2:
        zero_child_node, one_child_node = node[:2]
        zero_child_count, one_child_count = zero_child_node[2], one_child_node[2]

        # prefer 1 for most common if equal
        # prefer 0 for least common if equal
        if not (zero_child_node and one_child_node):
            node = one_child_node or zero_child_node
        elif zero_child_count > one_child_count:
            node = zero_child_node if preferred_bit == '1' else one_child_node
        else:
            node = zero_child_node if preferred_bit == '0' else one_child_node

    node = node[0] if preferred_bit == '0' else node[1]
    return find_only_leaf(node)


def search_driver(bitstrings):
    tree = prefix_tree(bitstrings)
    oxygen_rating = find_rating(tree, '1')
    carbon_rating = find_rating(tree, '0')
    def bin_to_int(bs):
        multiplier = 1
        acc = 0
        for b in bs[::-1]:
            if b == '1':
                acc += multiplier

            multiplier *= 2
        return acc

    return bin_to_int(oxygen_rating)*bin_to_int(carbon_rating)


