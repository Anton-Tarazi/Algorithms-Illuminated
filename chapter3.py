from itertools import combinations
from random import randint


def _count_split_inv(left, right):
    i, j, split_count = 0, 0, 0
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

        if left[i] <= right[j]:
            output.append(left[i])
            i += 1
        else:
            output.append(right[j])
            j += 1
            split_count += len(left) - i
    return output, split_count


def _count_inv(array):
    n = len(array)
    if n <= 1:
        return array, 0
    else:
        mid = n // 2
        left_sorted, left_inv = _count_inv(array[:mid])
        right_sorted, right_inv = _count_inv(array[mid:])
        merge_sorted, split_inv = _count_split_inv(left_sorted, right_sorted)
        return merge_sorted, left_inv + right_inv + split_inv


def count_inv(array):
    return _count_inv(array)[1]


def mat_mult(a, b):
    if len(a[0]) == len(b):
        n = len(b)
    else:
        raise ValueError("Rows of array don't match columns of B")

    out = []
    for i in range(n):
        out.append([])
        for j in range(n):
            new_entry = 0
            for k in range(n):
                new_entry += a[i][k] * b[k][j]
            out[i].append(new_entry)
    return out


x = [[1, 2], [3, 4]]
y = [[6, 7], [2, 2]]


def _distance(point_pair):
    if point_pair is None:
        return float('inf')
    p1 = point_pair[0]
    p2 = point_pair[1]
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def dist(point1, point2):
    return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2


def _closest_split_pair(x_sorted, y_sorted, delta):
    mid = len(x_sorted) // 2
    x_bar = x_sorted[mid][0]  # largest x coord in left half
    y_restricted = [point for point in y_sorted if x_bar - delta < point[0] < x_bar + delta]

    closest = None
    closest_distance = delta
    for i in range(len(y_restricted) - 1):
        for j in range(i + 1, min(i + 7, len(y_restricted))):
            if dist(y_restricted[i], y_restricted[j]) < closest_distance:
                closest_distance = dist(y_restricted[i], y_restricted[j])
                closest = (y_restricted[i], y_restricted[j])
    return closest


def _execute_closest_pair(x_sorted, y_sorted):
    n = len(x_sorted)
    if n <= 3:
        return min(combinations(x_sorted, 2), key=_distance)

    mid = n // 2
    lx = x_sorted[:mid]
    ly = y_sorted[:mid]
    rx = x_sorted[mid:]
    ry = y_sorted[mid:]

    # each of these is a list of two points (tuples)
    # ex [(1,2),(3,4)]
    best_left = _execute_closest_pair(lx, ly)
    best_right = _execute_closest_pair(rx, ry)

    smallest_so_far = _distance(min(best_left, best_right, key=_distance))
    best_split = _closest_split_pair(x_sorted, y_sorted, smallest_so_far)
    return min(best_left, best_right, best_split, key=_distance)


def closest_pair(points):
    """Computes the closest pair of points in an array of points (2D tuples)- runs in O(n log n)"""

    x_sorted = sorted(points, key=lambda x: x[0])
    y_sorted = sorted(points, key=lambda y: y[1])
    return _execute_closest_pair(x_sorted, y_sorted)


def unimodal_max(array):
    """Problem 3.3. Returns max element of uni-modal array. Takes O(log n) runtime"""
    mid = len(array) // 2
    check1 = mid - 1
    check2 = mid
    check3 = mid + 1
    if len(array) <= 2:
        return max(array)

    if array[check1] < array[check2] > array[check3]:
        return array[check2]
    elif array[check1] < array[check2] < array[check3]:
        return unimodal_max(array[check2:])
    elif array[check1] > array[check2] > array[check3]:
        return unimodal_max(array[:check2])


def equal_index(array, offset=0):
    """Algorithms Illuminated problem 3.4. Returns True/ False if sorted integer array has an element
    that is equal to its search_index. O(log n) runtime"""
    if len(array) == 0:
        return False

    index_to_check = len(array) // 2

    if array[index_to_check] == index_to_check + offset:
        return True
    elif array[index_to_check] < index_to_check + offset:
        offset += index_to_check + 1
        return equal_index(array[index_to_check + 1:], offset)
    else:
        return equal_index(array[:index_to_check], offset)


def inefficient_closest(points):
    closest = None
    closest_distance = float('inf')
    for i in range(0, len(points) - 1):
        for j in range(i + 1, len(points)):
            if dist(points[i], points[j]) < closest_distance:
                closest_distance = dist(points[i], points[j])
                closest = (points[i], points[j])
    return closest


test_points = [(randint(0, 100), randint(0, 100)) for i in range(10)]
print(test_points)
print(closest_pair(test_points))
print(inefficient_closest(test_points))
print(closest_pair(test_points) == inefficient_closest(test_points))
