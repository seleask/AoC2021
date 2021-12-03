

def depth(arr):
    total = 0

    for i,v in enumerate(arr[1:]):
        if v > arr[i]:
            total += 1

    return total

# now determine when the three element sliding window increases. The element we gain by sliding minus the element we lose by sliding tells us the difference in sums, so when this is positive we can count it. No need to keep the running total.

def sliding_depth(arr):

    total = 0
    for i in range(1,len(arr)-2):
        lost_elem = arr[i-1]
        gained_elem = arr[i+2]
        if (gained_elem - lost_elem) > 0:
            total += 1

    return total

