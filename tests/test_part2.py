from part2.chapter9 import UndirectedGraph, DirectedGraph
from part2.chapter10 import heap_median_maintenance_sum
from part2.chapter11 import bst_median_maintenance_sum
from part2.chapter12 import two_sum

from tests import generate_tests


# graph on page 38 of part 2
test_graph1 = UndirectedGraph()
test_graph1.add_edge_by_name(1, 3)
test_graph1.add_edge_by_name(1, 5)
test_graph1.add_edge_by_name(3, 5)
test_graph1.add_edge_by_name(5, 7)
test_graph1.add_edge_by_name(5, 9)
test_graph1.add_edge_by_name(2, 4)
test_graph1.add_edge_by_name(6, 8)
test_graph1.add_edge_by_name(6, 10)

# graph on page 33 of part 2
test_graph2 = UndirectedGraph()
test_graph2.add_edge_by_name(1, 2)
test_graph2.add_edge_by_name(1, 3)
test_graph2.add_edge_by_name(2, 4)
test_graph2.add_edge_by_name(3, 4)
test_graph2.add_edge_by_name(3, 6)
test_graph2.add_edge_by_name(4, 5)
test_graph2.add_edge_by_name(4, 6)
test_graph2.add_edge_by_name(5, 6)


def test_bfs():
    assert set(test_graph1.bfs(1)) == {1, 3, 5, 7, 9}
    assert set(test_graph1.bfs(2)) == {2, 4}
    assert set(test_graph1.bfs(6)) == {6, 8, 10}

    assert set(test_graph2.bfs(3)) == {1, 2, 3, 4, 5, 6}


def test_augmented_bfs():
    assert test_graph2.augmented_bfs(1) == {1: 0, 2: 1, 3: 1, 4: 2, 6: 2, 5: 3}


def test_connected_components():
    assert test_graph1.connected_components() == [[1, 3, 5, 7, 9], [2, 4], [6, 8, 10]]


def test_dfs():
    assert set(test_graph1.dfs(1)) == {1, 3, 5, 7, 9}
    assert set(test_graph1.dfs(2)) == {2, 4}
    assert set(test_graph1.dfs(6)) == {6, 8, 10}

    assert set(test_graph2.dfs(3)) == {1, 2, 3, 4, 5, 6}


def test_topo_sort():
    test_graph3 = DirectedGraph()
    test_graph3.add_edge_by_name(1, 2)
    test_graph3.add_edge_by_name(1, 3)
    test_graph3.add_edge_by_name(2, 4)
    test_graph3.add_edge_by_name(3, 4)

    assert test_graph3.topo_sort() == {1: 1, 2: 2, 3: 3, 4: 4} or \
           test_graph3.topo_sort() == {1: 1, 2: 3, 3: 2, 4: 4}
    assert test_graph3.topo_sort(reverse=True) == {1: 4, 2: 2, 3: 3, 4: 1} or \
           test_graph3.topo_sort(reverse=True) == {1: 4, 2: 3, 3: 2, 4: 1}


def test_strong_connected_components():
    scc_test1 = \
        generate_tests.create_directed_graph("../test_cases/part2_test_cases/problem8.10test1.txt")
    assert sorted(scc_test1.strong_connected_components()) == [3, 3, 3]

    scc_test2 = \
        generate_tests.create_directed_graph("../test_cases/part2_test_cases/problem8.10test2.txt")
    assert sorted(scc_test2.strong_connected_components()) == [2, 3, 3]

    scc_test3 = \
        generate_tests.create_directed_graph("../test_cases/part2_test_cases/problem8.10test3.txt")
    assert sorted(scc_test3.strong_connected_components()) == [1, 1, 3, 3]

    scc_test4 = \
        generate_tests.create_directed_graph("../test_cases/part2_test_cases/problem8.10test4.txt")
    assert sorted(scc_test4.strong_connected_components()) == [1, 7]

    scc_test5 = \
        generate_tests.create_directed_graph("../test_cases/part2_test_cases/problem8.10test5.txt")
    assert sorted(scc_test5.strong_connected_components()) == [1, 2, 3, 6]


dijkstra_test1 = \
    generate_tests.create_dijkstra_graph("../test_cases/part2_test_cases/problem9.8test.txt")
dijkstra_test2 = \
    generate_tests.create_dijkstra_graph("../test_cases/part2_test_cases/problem9.8.txt")


def test_dijkstra():
    assert dijkstra_test1.dijkstra(1) == \
           {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 4, 7: 3, 8: 2}

    # reference values from
    # https://github.com/claytonjwong/Algorithms-Illuminated/blob/main/dijkstra/main.py
    test2_dict = dijkstra_test2.dijkstra(1)
    assert test2_dict[7] == 2599
    assert test2_dict[37] == 2610
    assert test2_dict[59] == 2947
    assert test2_dict[82] == 2052
    assert test2_dict[99] == 2367
    assert test2_dict[115] == 2399
    assert test2_dict[133] == 2029
    assert test2_dict[165] == 2442
    assert test2_dict[188] == 2505
    assert test2_dict[197] == 3068


def test_dijkstra_2():
    assert dijkstra_test1.dijkstra_2(1) == \
           {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 4, 7: 3, 8: 2}

    # compare second implementation to first implementation, which is compared to
    # solution found online
    assert dijkstra_test2.dijkstra_2(1) == dijkstra_test2.dijkstra(1)


def test_efficient_dijkstra():
    assert dijkstra_test1.efficient_dijkstra(1) == \
           {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 4, 7: 3, 8: 2}

    # compare fast implementation accuracy to slow implementation
    assert dijkstra_test2.efficient_dijkstra(1) == \
           dijkstra_test2.dijkstra(1)


med_main_test1 = \
    generate_tests.create_list("../test_cases/part2_test_cases/problem11.3test.txt")
med_main_test2 = \
    generate_tests.create_list("../test_cases/part2_test_cases/problem11.3.txt")


def test_heap_median_maintenance_sum():
    assert heap_median_maintenance_sum(med_main_test1) % 10000 == 9335
    assert heap_median_maintenance_sum(med_main_test2) % 10000 == 1213


def test_bst_median_maintenance_sum():
    assert bst_median_maintenance_sum(med_main_test1) % 10000 == 9335
    assert bst_median_maintenance_sum(med_main_test2) % 10000 == 1213


def test_two_sum():
    two_sum_test1 = generate_tests.create_list("../test_cases/part2_test_cases/problem12.4test.txt")
    assert two_sum(two_sum_test1, range(3, 11)) == 8
