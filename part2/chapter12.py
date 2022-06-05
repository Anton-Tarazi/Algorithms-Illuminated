def two_sum(array, target_range):
    """Returns number of distinct pairs of entries in an array
    sum to a value contained in the target range"""

    # initialize a hash table with the contents of the array
    hash_table = {}
    for entry in array:
        hash_table[entry] = True

    counter = 0
    for target in target_range:

        # for any x check if the y such that x + y = target is in the hash table
        # and make sure they are distinct
        for x in array:
            y = target - x
            if y != x and hash_table.get(y) is not None:
                counter += 1
                break
    return counter

