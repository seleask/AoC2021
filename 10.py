def read_nav_file(f):
    lines = open(f).read().split('\n')
    return lines

open_parens = "([{<"
close_parens = ")]}>"

closed_from_open = {k:v for k,v in zip(open_parens, close_parens)}
open_from_closed = {k:v for v,k in closed_from_open.items()}

paren_scores = {k:v for k,v in zip(close_parens, [3, 57, 1197, 25137])}

# return first bad closing paren if corrupt, or the missing closing parens (stack) if incomplete
def corrupt_or_incomplete(line):
    stack = []

    for c in line:
        if c in open_parens:
            stack.append(closed_from_open.get(c))
        elif c in close_parens:
            head = stack[-1]
            if head != c:
                return c
            else:
                stack.pop()

    return stack

### Part 1 ###

def first_bad_closing_paren(line):
    result = corrupt_or_incomplete(line)
    if isinstance(result, str):
        return result

def score_corrupt_lines(lines):
    total = 0

    for line in lines:
        bad_paren = first_bad_closing_paren(line)

        total += paren_scores.get(bad_paren, 0)

    return total

def score_corrupt_nav_file(f):
    return score_corrupt_lines(read_nav_file(f))

### Part 2 ###

completion_paren_scores = {k:v for k,v in zip(close_parens, range(1,5))}

def completion_string_for_line(line):
    result = corrupt_or_incomplete(line)
    if isinstance(result, list):
        return "".join(result[::-1])

def completion_strings(lines):
    return list(filter(None, map(completion_string_for_line, lines)))

def score_completion(completion):
    total = 0
    for closing_paren in completion:
        total *= 5
        total += completion_paren_scores.get(closing_paren)

    return total

def score_complete_lines(all_lines):
    completions = completion_strings(all_lines)
    scores = list(map(score_completion, completions))
    return sorted(scores)[len(scores)//2]

def score_complete_nav_file(f):
    return score_complete_lines(read_nav_file(f))
