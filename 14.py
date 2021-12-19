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

def expand_template_old(template, rules):
    insertions = insertions_for_template(template, rules)

    result = []
    for i in range(len(insertions)):
        result.append(template[i])
        result.append(insertions[i])

    result.append(template[-1])

    return "".join(result)


def expand_template_n(n, template, rules):
    for _ in range(n):
        template = expand_template_old(template, rules)

    return template

def solve_polymer(n, template, rules):
    polymer = expand_template_n(n, template, rules)
    counts = Counter(polymer)
    most_common = counts.most_common(1)[0][1]
    least_common = counts.most_common()[-1][1]
    return counts.most_common(1)[0][1] - counts.most_common()[-1][1]


## Part 2 (second attempt, avoid explicitly representing pairs
## this works

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


## Part 2 again (try to get the DP-style approach working at last)
# this also works, but not as fast

def expand_pairs_n(n, pair, rules, cache={}):
    if n == 0:
        return Counter()

    l,r = pair

    if (l,r,n) in cache:
        return cache[(l,r,n)]

    key = l+r
    c = rules[key]

    count_map = Counter()
    count_map[c] += 1

    counts_l = expand_pairs_n(n-1, (l+c), rules, cache)
    counts_r = expand_pairs_n(n-1, (c+r), rules, cache)

    count_map = count_map + counts_l + counts_r

    cache[(l,r,n)] = count_map
    return count_map

def expand_template(n, template, rules):
    count_map = Counter(template)

    cache = {}
    for cm in [expand_pairs_n(n, pair, rules, cache) for pair in zip(template, template[1:])]:
        count_map += cm
    return count_map

def solve(n, template, rules):
    count_map = expand_template(n, template, rules)
    most_common = count_map.most_common(1)[0][1]
    least_common = count_map.most_common()[-1][1]
    return most_common - least_common
