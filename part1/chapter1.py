def merge(left, right):
    i, j = 0, 0
    output = []
    for k in range(len(left) + len(right)):
        if i >= len(left):
            output.append(right[j])
            j += 1
            continue
        if j >= len(right):
            output.append(left[i])
            i += 1
            continue

        if left[i] < right[j]:
            output.append(left[i])
            i += 1
        else:
            output.append(right[j])
            j += 1
    return output


def mergesort(array):
    n = len(array)
    if n <= 1:
        return array

    sorted_left = mergesort(array[:n//2])
    sorted_right = mergesort(array[n//2:])
    return merge(sorted_left, sorted_right)
