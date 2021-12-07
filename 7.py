def fuel_cost(crabs, position):
    return sum(map(lambda crab: abs(crab-position), crabs))


def fuel_cost_2(crabs, position):
    sum_nat = lambda diff: diff*(diff+1) // 2
    return sum(map(lambda crab: sum_nat(abs(crab-position)), crabs))


def cheapest_fuel(crabs, fuel_cost_fn):
    # start with mean position as initial guess
    guess = sum(crabs) // len(crabs)

    # inverted hill climb
    left_cost, guess_cost, right_cost = map(lambda guess: fuel_cost_fn(crabs, guess), [guess-1, guess, guess+1])
    leftmost, rightmost = min(crabs), max(crabs)

    if guess == leftmost:
        guess += 1

    if guess == rightmost:
        guess -= 1

    while leftmost < guess < rightmost:
        left_guess, right_guess = guess-1, guess+1

        if left_cost < guess_cost:
            guess -= 1
            left_cost, guess_cost, right_cost = fuel_cost_fn(crabs, guess-1), left_cost, guess_cost
        elif right_cost < guess_cost:
            guess += 1
            left_cost, guess_cost, right_cost = guess_cost, right_cost, fuel_cost_fn(crabs, guess+1)
        else:
            break

    return guess_cost


cheapest_fuel_1 = lambda crabs: cheapest_fuel(crabs, fuel_cost)
cheapest_fuel_2 = lambda crabs: cheapest_fuel(crabs, fuel_cost_2)
