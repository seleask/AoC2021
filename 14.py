from collections import Counter, defaultdict

def read_polymer_system(f):
    template, rules_str = open(f).read().split("\n\n")
    rule_strings = rules_str.split('\n')[:-1]

    return template, \
        {rule[0]:rule[1] for rule in map(lambda rs: rs.split(" -> "), rule_strings)}


## Part 1 (naive)

def insertions_for_template(template, rules):
    insertions = []
    for a,b in zip(template, template[1:]):
        r = rules.get(a+b)
        if r:
            print("inserting", r, "for match:", a+b)
        insertions.append(rules.get(a+b, ""))

    print(insertions)
    return insertions

def expand_template(template, rules):
    insertions = insertions_for_template(template, rules)

    result = []
    for i in range(len(insertions)):
        result.append(template[i])
        result.append(insertions[i])

    result.append(template[-1])

    return "".join(result)


def expand_template_n(n, template, rules):
    for _ in range(n):
        template = expand_template(template, rules)

    return template

def solve_polymer(n, template, rules):
    polymer = expand_template_n(n, template, rules)
    counts = Counter(polymer)
    most_common = counts.most_common(1)[0][1]
    least_common = counts.most_common()[-1][1]
    return counts.most_common(1)[0][1] - counts.most_common()[-1][1]


## Part 2 (first attempt, too slow but better with space)

def expand_pair(pair, depth, rules):
    l,r = pair
    c = rules.get(l+r)

    return c,(l,c,depth+1),(c,r,depth+1)

def expand_pairs_n(n, pairs, rules):
    count_map = defaultdict(int)

    stack = [(pair[0],pair[1],0) for pair in pairs]

    while stack:
        l,r,depth = stack.pop()
        if depth == n:
            continue

        c, l_pair, r_pair = expand_pair((l,r), depth, rules)

        count_map[c] += 1
        stack.append(l_pair)
        stack.append(r_pair)

    return count_map

def expand_template_n_new(n, template, rules):
    pairs = zip(template, template[1:])

    count_map = expand_pairs_n(n, pairs, rules)
    for c in template:
        count_map[c] += 1

    return count_map

def solve_polymer_new(n, template, rules):
    count_map = expand_template_n_new(n, template, rules)
    most_common = count_map[template[0]]
    least_common = most_common

    for count in count_map.values():
        most_common = max(most_common, count)
        least_common = min(least_common, count)

    return most_common-least_common

## Part 2 (second attempt, avoid explicitly representing pairs)

def solve_polymer_best(n, template, rules):
    template_pairs = zip(template, template[1:])
    pair_count_map = Counter()

    for l,r in template_pairs:
        pair_count_map[l+r] += 1

    for i in range(n-1):
        count_map = Counter()
        for k,v in pair_count_map.items():
            l,r = k
            c = rules.get(k)

            count_map[l+c] += v
            count_map[c+r] += v

        pair_count_map = count_map

    char_count_map = Counter()
    for k,v in pair_count_map.items():
        l,r = k
        c = rules.get(k)

        char_count_map[l] += v
        char_count_map[c] += v

    char_count_map[template[-1]] += 1

    most_common = char_count_map.most_common(1)[0][1]
    least_common = char_count_map.most_common()[-1][1]
    return most_common - least_common
