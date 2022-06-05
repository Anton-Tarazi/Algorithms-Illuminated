from itertools import combinations


def _count_split_inv(left, right):
    """Helper function to count_inv. Based on merge subroutine of mergesort and counts all instances
    of the right array having elements larger than left array"""

    # i is a counter for the left list, j is a counter for the right list, and
    # split_count keeps track of how many split pairs there are between the left
    # and right lists
    i, j, split_count = 0, 0, 0
    output = []
    # iterate through all elements of both lists
    for k in range(len(left) + len(right)):

        # if we've passed the end of the left list add all the remaining elements
        # of the right list to the output and increment j accordingly
        if i >= len(left):
            output.append(right[j])
            j += 1
            continue
        # if we've passed the end of the right  list add all the remaining elements
        # of the left list to the output and increment i accordingly
        if j >= len(right):
            output.append(left[i])
            i += 1
            continue

        # append smaller element to output list
        if left[i] <= right[j]:
            output.append(left[i])
            i += 1
        else:
            output.append(right[j])
            j += 1
            # if smaller element is in the right list, we have as many inversions as there are
            # elements remaining in the left list
            split_count += len(left) - i
    return output, split_count


def _count_inv(array):
    """Helper function for count_inv. Based on mergesort: recursively counts inversions in
    left half of array, right half of array, and inversions between the two"""
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
    # we only look at a subset of the points, those within delta of the midline, where delta
    # is the closest distance that has already been found in the left or right halves
    y_restricted = [point for point in y_sorted if x_bar - delta < point[0] < x_bar + delta]

    # determine the closest pair within this subset, or return None if there is no pair
    # that has a distance less than delta
    closest = None
    closest_distance = delta
    for i in range(len(y_restricted) - 1):
        for j in range(i + 1, min(i + 7, len(y_restricted))):
            if dist(y_restricted[i], y_restricted[j]) < closest_distance:
                closest_distance = dist(y_restricted[i], y_restricted[j])
                closest = (y_restricted[i], y_restricted[j])
    return closest


def _execute_closest_pair(x_sorted, y_sorted):
    """Recursive helper function for closest pair"""
    n = len(x_sorted)

    # base case of 3: find the closest pair by exhaustive search
    if n <= 3:
        return min(combinations(x_sorted, 2), key=_distance)

    mid = n // 2
    lx = x_sorted[:mid]
    ly = y_sorted[:mid]
    rx = x_sorted[mid:]
    ry = y_sorted[mid:]

    # find the closest pair in the left half of the points, and the closest pair in the right half
    # each of these is a list of two points (tuples), ex. [(1,2),(3,4)]
    best_left = _execute_closest_pair(lx, ly)
    best_right = _execute_closest_pair(rx, ry)

    # record the distance between the closest pair found within the left half or the right half
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
    """Compute closest pair via exhaustive search- O(n^2) runtime. Purpose of this function is
    a comparison to check correctness of the efficient implementation of closest pair"""
    closest = None
    closest_distance = float('inf')
    for i in range(0, len(points) - 1):
        for j in range(i + 1, len(points)):
            if dist(points[i], points[j]) < closest_distance:
                closest_distance = dist(points[i], points[j])
                closest = (points[i], points[j])
    return closest

