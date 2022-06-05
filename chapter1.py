import random


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


def second_largest_number(array):
    """Returns the second-largest number of an unsorted array of n distinct numbers, where
    n is a power of 2- does at most n + log n - 2 comparisons"""
    largest = -float('inf')
    second_largest = -float('inf')
    for i in array:
        if i > largest:
            second_largest = largest
            largest = i
        elif i > second_largest:
            second_largest = i
    return second_largest


def two_sum(nums, target):
    nums_dict = {}
    for index, num in enumerate(nums):
        nums_dict[num] = index

    for ind, n in enumerate(nums):
        goal = target - n
        if goal != n and nums_dict.get(goal) is not None:
            return [ind, nums_dict[goal]]


print(mergesort([random.randint(0, 100) for i in range(10000)]))
print(mergesort([5,2,3,4]))