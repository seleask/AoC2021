from collections import defaultdict


def parse_into_graph(lines):
    graph = defaultdict(list)
    for line in lines:
        left, right = line.split('-')
        graph[left] += [right]
        graph[right] += [left]

    return graph


def file_into_graph(f):
    lines = open(f).read().split('\n')
    return parse_into_graph(lines[:-1])


def is_big_cave(node):
    return node.isupper()


def count_paths_helper(graph, node, small_cs, visited, path):
    if not is_big_cave(node):
        visited[node] = True
    path.append(node)

    path_counter = 0
    if node == "end":
        path_counter = 1
    else:
        for reachable in graph[node]:
            if not visited[reachable] or reachable in small_cs and not any(path.count(c) >= 2 for c in small_cs):
                path_counter += count_paths_helper(graph, reachable, small_cs, visited, path)

    path.pop()
    if path.count(node) == 0:
        visited[node] = False
    return path_counter


# Part 1
def count_paths(graph):
    visited = defaultdict(bool)
    path = []

    return count_paths_helper(graph, "start", [], visited, path)


def small_caves(graph):
    caves = [k for k in graph.keys() if not k.isupper()]
    caves.remove('start')
    caves.remove('end')
    return caves


# Part 2
def count_paths_double_dip(graph):
    visited = defaultdict(bool)
    path = []

    return count_paths_helper(graph, "start", small_caves(graph), visited, path)
