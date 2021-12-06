def initial_fish_array(fish):
    arr = [0]*7
    for f in fish:
        arr[f] += 1

    return arr

def update_population(fish_arr, fish_i, spawned_arr, spawned_i):
    new_adults_to_move = spawned_arr[spawned_i]
    new_adults_i = fish_i-1

    fish_arr[new_adults_i] += new_adults_to_move

    fish_to_spawn = fish_arr[fish_i]
    spawned_arr[spawned_i] = fish_to_spawn


def simulate_days(fish, n):
    fish_arr = initial_fish_array(fish)
    spawned_arr = [0]*3
    fish_i = spawned_i = 0

    for _ in range(n):
        update_population(fish_arr, fish_i, spawned_arr, spawned_i)
        fish_i = (fish_i+1) % len(fish_arr)
        spawned_i = (spawned_i+1) % len(spawned_arr)

    return sum(fish_arr)+sum(spawned_arr)
