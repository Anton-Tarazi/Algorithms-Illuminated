from part1.chapter1 import mergesort
from part1.chapter3 import count_inv, closest_pair, inefficient_closest
from part1.chapter5 import quicksort, left_pivot, right_pivot, median_pivot
from part1.chapter6 import select

from tests import generate_tests


def test_mergesort():
    array1 = [58, 32, 12, 100, 66, 19, 2, 28, 29, 75, 72]
    assert mergesort(array1) == sorted(array1)

    array2 = [0, -23, 29, 105, 293, -44, -312, 56, 65, 33, 41]
    assert mergesort(array2) == sorted(array2)

    array3 = [5.6, 4.331, 10.11, 2.21, -0.8, 4.2, 6.778, -12.1, -8.43]
    assert mergesort(array3) == sorted(array3)


def test_count_inv():
    array1 = list(range(1, 10))
    assert count_inv(array1) == 0

    array2 = list(range(10, 0, -1))
    assert count_inv(array2) == 45

    count_inv_test1 = generate_tests.create_list("../test_cases/part1_test_cases/problem3.5test.txt")
    assert count_inv(count_inv_test1) == 28

    count_inv_test2 = generate_tests.create_list("../test_cases/part1_test_cases/problem3.5.txt")
    assert count_inv(count_inv_test2) == 2407905288


def test_closest_pair():
    # note we check the reversed order as well because the two closest pair
    # functions may return the pair in different orders
    points1 = [(46, 16), (15, 65), (30, 100), (4, 28), (90, 54), (90, 58),
               (95, 30), (34, 48), (13, 53), (93, 86)]
    assert closest_pair(points1) == \
           inefficient_closest(points1) or inefficient_closest(points1)[::-1]

    points2 = [(3, 81), (20, 30), (9, 48), (72, 83), (28, 20), (100, 21),
               (22, 12), (74, 40), (81, 76), (60, 12)]
    assert closest_pair(points2) == \
           inefficient_closest(points2) or inefficient_closest(points2)[::-1]

    points3 = [(7, 13), (55, 42), (12, 75), (70, 75), (9, 20), (56, 27),
               (4, 94), (8, 20), (83, 100), (96, 30)]
    assert closest_pair(points3) == \
           inefficient_closest(points3) or inefficient_closest(points3)[::-1]


def test_quicksort():
    array1 = [22, 18, 21, 2, -18, -19, 16, -8, 6, -5]
    assert quicksort(array1) == sorted(array1)

    quicksort_test1 = \
        generate_tests.create_list("../test_cases/part1_test_cases/problem5.6test1.txt")
    assert quicksort(quicksort_test1.copy(),
                     pivot_choice=left_pivot, num_steps=True) == 25
    assert quicksort(quicksort_test1.copy(),
                     pivot_choice=right_pivot, num_steps=True) == 31
    assert quicksort(quicksort_test1.copy(),
                     pivot_choice=median_pivot, num_steps=True) == 21

    quicksort_test2 = \
        generate_tests.create_list("../test_cases/part1_test_cases/problem5.6test2.txt")
    assert quicksort(quicksort_test2.copy(),
                     pivot_choice=left_pivot, num_steps=True) == 620
    assert quicksort(quicksort_test2.copy(),
                     pivot_choice=right_pivot, num_steps=True) == 573
    assert quicksort(quicksort_test2.copy(),
                     pivot_choice=median_pivot, num_steps=True) == 502


def test_select():
    array1 = [7, 3, 2, 10, 5, 4, 1, 6, 9, 8]
    assert select(array1, 5) == 5

    select_test1 = \
        generate_tests.create_list("../test_cases/part1_test_cases/problem6.5test1.txt")
    assert select(select_test1, 5) == 5469

    select_test2 = \
        generate_tests.create_list("../test_cases/part1_test_cases/problem6.5test2.txt")
    assert select(select_test2, 50) == 4715
