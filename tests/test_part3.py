from tests import generate_tests
from part3.chapter13 import sum_weighted_completion_times, greedy_difference, greedy_ratio
from part3.chapter14 import huffman_code, min_max_encoding_lengths
from part3.chapter16 import KnapsackItem, max_ind_set, \
    wis_reconstruction, knapsack_value, knapsack_reconstruction
from part3.chapter17 import nw_score, reconstruction, verify_reconstruction, \
    optimal_binary_search_tree, efficient_optimal_bst

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
    generate_tests.create_mst_graph("../test_cases/part3_test_cases/problem15.9test.txt")

mst_test2 = \
    generate_tests.create_mst_graph("../test_cases/part3_test_cases/problem15.9.txt")


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


def test_efficient_kruskal():
    tree1 = mst_test1.efficient_kruskal()
    assert tree1.size() == 14

    tree2 = mst_test2.efficient_kruskal()
    assert tree2.size() == -3612829


def test_max_ind_set():
    graph_test1 = generate_tests.create_list("../test_cases/part3_test_cases/problem16.6test.txt")
    assert max_ind_set(graph_test1) == 2617
    assert wis_reconstruction(graph_test1) == {2, 4, 7, 10}

    graph_test2 = generate_tests.create_list("../test_cases/part3_test_cases/problem16.6.txt")
    assert max_ind_set(graph_test2) == 2955353732


def test_knapsack():
    knapsack_test1 = \
        generate_tests.create_knapsack_item_list("../test_cases/part3_test_cases/problem16.7test.txt")
    assert knapsack_value(10000, knapsack_test1) == 2493893

    knapsack_test2 = [KnapsackItem(3, 4), KnapsackItem(2, 3), KnapsackItem(4, 2), KnapsackItem(4, 3)]
    assert knapsack_value(6, knapsack_test2) == 8
    assert knapsack_reconstruction(6, knapsack_test2) == {3, 4}

    knapsack_test3 = [KnapsackItem(1, 1), KnapsackItem(2, 3), KnapsackItem(3, 2),
                      KnapsackItem(4, 5), KnapsackItem(5, 4)]
    assert knapsack_value(9, knapsack_test3) == 10
    assert knapsack_reconstruction(9, knapsack_test3) == {2, 3, 5}


def test_sequence_alignment():
    sequence_test1 = \
        generate_tests.create_sequences("../test_cases/part3_test_cases/problem17.8nw.txt")

    assert nw_score(sequence_test1, 4, 5) == 224

    aligned_sequences = reconstruction(sequence_test1, 4, 5)
    assert aligned_sequences == \
           ('ACACATGCATCATGACTATGCATGCATGACTGACTGCATGCATGCATCCATCATGCATGCATCGATGCATGCATGAC-'
            'CAC-C-TGTGT-GACA-CATGCATGCGTG--TGACATGCGAGACTCACTAGCGATGCATGC-ATGCATGCATGCATGC',
            'A----TG-ATCATG-C-ATGCATGCATCAC--ACTG--TGCAT-CAGAGAG-A-GC-T-C-TC-A-GCA-G-ACCACACA'
            'CACGTGTGCAGAGAGCATGCATGCATGCATG-CATGC-A---TGG-TAGC--TGCATGCTATG-A-GCATGCA-G-')

    assert verify_reconstruction(aligned_sequences, 4, 5) == 224


opbst_test2 = \
    generate_tests.create_frequencies("../test_cases/part3_test_cases/problem17.8optbst.txt")


def test_optimal_binary_search_tree():
    assert optimal_binary_search_tree(opbst_test2) == 2780


def test_efficient_optimal_bst():
    assert efficient_optimal_bst(opbst_test2) == 2780



