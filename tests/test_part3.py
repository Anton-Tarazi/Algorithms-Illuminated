from tests import generate_tests
from part3.chapter13 import sum_weighted_completion_times, greedy_difference, greedy_ratio
from part3.chapter14 import huffman_code, min_max_encoding_lengths
from part3.chapter15 import SpanningTree


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


def test_huffman_codes():
    alphabet1 = generate_tests.create_alphabet("../test_cases/part3_test_cases/problem14.6test1.txt")
    huffman_code1 = huffman_code(alphabet1)
    assert min_max_encoding_lengths(huffman_code1) == (2, 5)

    alphabet2 = generate_tests.create_alphabet("../test_cases/part3_test_cases/problem14.6test2.txt")
    huffman_code2 = huffman_code(alphabet2)
    assert min_max_encoding_lengths(huffman_code2) == (3, 6)

    # compared solution to
    # https://github.com/claytonjwong/Algorithms-Illuminated/blob/main/huffman/main.py
    alphabet3 = generate_tests.create_alphabet("../test_cases/part3_test_cases/problem14.6.txt")
    huffman_code3 = huffman_code(alphabet3)
    assert min_max_encoding_lengths(huffman_code3) == (9, 19)


mst_test1 = \
    generate_tests.create_prim_graph("../test_cases/part3_test_cases/problem15.9test.txt")

mst_test2 = \
    generate_tests.create_prim_graph("../test_cases/part3_test_cases/problem15.9.txt")


def test_prim():
    tree1 = mst_test1.prim()
    tree1.display()
    assert tree1.size() == 14

    # solution from https://github.com/claytonjwong/Algorithms-Illuminated/blob/main/prim/main.py
    tree2 = mst_test2.prim()
    assert tree2.size() == -3612829


def test_efficient_prim():
    tree1 = mst_test1.efficient_prim()
    assert tree1.size() == 14

    tree2 = mst_test2.efficient_prim()
    assert tree2.size() == -3612829


def test_kruskal():
    tree1 = mst_test1.kruskal()
    assert tree1.size() == 14

    tree2 = mst_test2.kruskal()
    assert tree2.size() == -3612829
