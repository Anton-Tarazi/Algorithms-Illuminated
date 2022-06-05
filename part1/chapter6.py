from part1.chapter5 import _partition


def _select(array, search_index, left, right):

    if left >= right:
        return array[left]

    pivot_index = _partition(array, left, right)

    if pivot_index - left == search_index - 1:
        return array[pivot_index]
    elif pivot_index - left > search_index - 1:
        return _select(array, search_index, left, pivot_index - 1)
    else:
        return _select(array, search_index - pivot_index + left - 1, pivot_index + 1, right)


def select(array, index):
    return _select(array, index, 0, len(array) - 1)



