import get_tests
from chapter13 import sum_weighted_completion_times, greedy_ratio, greedy_difference


def test_greedy_difference():
    assert sum_weighted_completion_times(
        greedy_difference(get_tests.greedy_scheduling_test1)) == 68615