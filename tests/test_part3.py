from tests import generate_tests
from part3.chapter13 import sum_weighted_completion_times, greedy_difference, greedy_ratio


greedy_scheduling_test1 = \
    generate_tests.create_job_list("../test_cases/part3_test_cases/problem13.4test.txt")
greedy_scheduling_test2 = \
    generate_tests.create_job_list("../test_cases/part3_test_cases/problem13.4.txt")


def test_greedy_difference():
    difference_schedule1 = greedy_difference(greedy_scheduling_test1)

    # these two entries have the same (weight - length value), but the way the
    # sorting algorithm breaks this tie gives a different answer from the one online,
    # so we swap them for consistency
    difference_schedule1[8], difference_schedule1[9] = \
        difference_schedule1[9], difference_schedule1[8]
    assert sum_weighted_completion_times(difference_schedule1) == 68615

    # not comparing this value to one found online because there are so many
    # ties between (weight - length) that could have yielded difference answers
    # depending on how they are ordered
    difference_schedule2 = greedy_difference(greedy_scheduling_test2)
    assert sum_weighted_completion_times(difference_schedule2) == 69120882574


def test_greedy_ratio():
    ratio_schedule1 = greedy_ratio(greedy_scheduling_test1)
    assert sum_weighted_completion_times(ratio_schedule1) == 67247

    # reference value from
    # https://github.com/claytonjwong/Algorithms-Illuminated/blob/main/greedy_scheduling/main.py
    ratio_schedule2 = greedy_ratio(greedy_scheduling_test2)
    assert sum_weighted_completion_times(ratio_schedule2) == 67311454237
