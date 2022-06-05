import random


def _partition(array, left, right):
    pivot = array[left]
    i = left + 1
    for j in range(left + 1, right + 1):
        if array[j] < pivot:
            array[j], array[i] = array[i], array[j]
            i += 1
    array[left], array[i - 1] = array[i - 1], array[left]
    return i - 1


def left_pivot(array, left, right):
    return left


def right_pivot(array, left, right):
    return right


def random_pivot(array, left, right):
    return random.randint(left, right - 1)


def median_pivot(array, left, right):
    left_index_and_value = (left, array[left])
    right_index_and_value = (right, array[right])
    midpoint = (left + right) // 2
    midpoint_index_and_value = (midpoint, array[midpoint])
    indices_and_values = [left_index_and_value, midpoint_index_and_value, right_index_and_value]
    return sorted(indices_and_values, key=lambda x: x[1])[1][0]


def _quicksort(array, left, right, choose_pivot):

    if left >= right:
        return 0, array

    i = choose_pivot(array, left, right)
    array[left], array[i] = array[i], array[left]

    j = _partition(array, left, right)
    num_steps = right - left
    num_steps += _quicksort(array, left, j - 1, choose_pivot)[0]
    num_steps += _quicksort(array, j + 1, right, choose_pivot)[0]

    return num_steps, array


def quicksort(array, pivot_choice=random_pivot, num_steps=False):
    l = 0
    r = len(array)
    if num_steps:
        return _quicksort(array, l, r - 1, pivot_choice)[0]
    else:
        return _quicksort(array, l, r - 1, pivot_choice)[1]


