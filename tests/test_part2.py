from tests import get_tests
from part2.chapter9 import UndirectedGraph, DirectedGraph
from part2.chapter10 import heap_median_maintenance_sum
from part2.chapter11 import bst_median_maintenance_sum
from part2.chapter12 import two_sum

test_graph1 = UndirectedGraph()
test_graph1.add_edge_by_name(1, 3)
test_graph1.add_edge_by_name(1, 5)
test_graph1.add_edge_by_name(3, 5)
test_graph1.add_edge_by_name(5, 7)
test_graph1.add_edge_by_name(5, 9)
test_graph1.add_edge_by_name(2, 4)
test_graph1.add_edge_by_name(6, 8)
test_graph1.add_edge_by_name(6, 10)

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
    test_graph4 = DirectedGraph()
    test_graph4.add_edge_by_name(1, 3)
    test_graph4.add_edge_by_name(3, 5)
    test_graph4.add_edge_by_name(5, 1)
    test_graph4.add_edge_by_name(3, 11)
    test_graph4.add_edge_by_name(5, 9)
    test_graph4.add_edge_by_name(5, 7)
    test_graph4.add_edge_by_name(7, 9)
    test_graph4.add_edge_by_name(11, 6)
    test_graph4.add_edge_by_name(11, 8)
    test_graph4.add_edge_by_name(9, 8)
    test_graph4.add_edge_by_name(9, 4)
    test_graph4.add_edge_by_name(4, 7)
    test_graph4.add_edge_by_name(9, 2)
    test_graph4.add_edge_by_name(2, 10)
    test_graph4.add_edge_by_name(2, 4)
    test_graph4.add_edge_by_name(6, 10)
    test_graph4.add_edge_by_name(10, 8)
    test_graph4.add_edge_by_name(8, 6)

    assert sorted(test_graph4.strong_connected_components()) == [1, 3, 3, 4]

    assert sorted(get_tests.scc_test1.strong_connected_components()) == [3, 3, 3]
    assert sorted(get_tests.scc_test2.strong_connected_components()) == [2, 3, 3]
    assert sorted(get_tests.scc_test3.strong_connected_components()) == [1, 1, 3, 3]
    assert sorted(get_tests.scc_test4.strong_connected_components()) == [1, 7]
    assert sorted(get_tests.scc_test5.strong_connected_components()) == [1, 2, 3, 6]


def test_dijkstra():
    assert get_tests.dijkstra_test1.dijkstra(1) == \
           {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 4, 7: 3, 8: 2}

    # reference values from
    # https://github.com/claytonjwong/Algorithms-Illuminated/blob/main/dijkstra/main.py
    test2_dict = get_tests.dijkstra_test2.dijkstra(1)
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
    assert get_tests.dijkstra_test1.dijkstra_2(1) == \
           {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 4, 7: 3, 8: 2}

    # compare second implementation to first implementation, which is compared to
    # solution found online
    assert get_tests.dijkstra_test2.dijkstra_2(1) == get_tests.dijkstra_test2.dijkstra(1)


def test_efficient_dijkstra():
    assert get_tests.dijkstra_test1.efficient_dijkstra(1) == \
           {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 4, 7: 3, 8: 2}

    # compare fast implementation to slow implementation
    assert get_tests.dijkstra_test2.efficient_dijkstra(1) == get_tests.dijkstra_test2.dijkstra(1)


def test_heap_median_maintenance_sum():
    assert heap_median_maintenance_sum(get_tests.med_main_test1) % 10000 == 9335
    assert heap_median_maintenance_sum(get_tests.med_main_test2) % 10000 == 1213


def test_bst_median_maintenance_sum():
    assert bst_median_maintenance_sum(get_tests.med_main_test1) % 10000 == 9335
    assert bst_median_maintenance_sum(get_tests.med_main_test2) % 10000 == 1213


def test_two_sum():
    assert two_sum(get_tests.two_sum_test1, range(3, 11)) == 8
