from dataclasses import dataclass


def max_ind_set(vertex_set: list[int]) -> int:
    """Returns the weight of the maximum weighted independent set of a path graph
    in O(n) runtime"""
    subproblems = [0, vertex_set[0]]
    for i in range(1, len(vertex_set)):
        subproblems.append(
            max(subproblems[-1], subproblems[-2] + vertex_set[i]))

    return subproblems[-1]


def wis_reconstruction(vertex_set: list[int]) -> set[int]:
    """Returns the vertices of the maximum weighted independent set of a path graph
    in O(n) runtime"""
    subproblems = [0, vertex_set[0]]
    for i in range(1, len(vertex_set)):
        subproblems.append(
            max(subproblems[-1], subproblems[-2] + vertex_set[i]))

    vertices_in_max_ind_set = set()
    i = len(vertex_set)
    while i >= 2:
        if subproblems[i - 1] >= subproblems[i - 2] + vertex_set[i - 1]:
            i -= 1
        else:
            vertices_in_max_ind_set.add(i)
            i -= 2
    if i == 1:
        vertices_in_max_ind_set.add(1)
    return vertices_in_max_ind_set


@dataclass
class KnapsackItem:
    value: int
    weight: int


def knapsack(capacity: int, items: list[KnapsackItem]) -> list[list[int]]:
    subproblems = [[0] * (capacity + 1)]

    for item in items:
        subproblems.append([])
        for c in range(capacity + 1):
            if item.weight > c:
                subproblems[-1].append(subproblems[-2][c])
            else:
                winner = max(subproblems[-2][c], subproblems[-2][c - item.weight] + item.value)
                subproblems[-1].append(winner)

    return subproblems


def knapsack_value(capacity: int, items: list[KnapsackItem]) -> int:
    return knapsack(capacity, items)[-1][-1]


def knapsack_reconstruction(capacity: int, items: list[KnapsackItem]) -> set[int]:
    subproblem_array = knapsack(capacity, items)

    best_items = set()
    c = capacity
    for i in range(len(items) - 1, -1, -1):
        item = items[i]
        if item.weight <= c:
            if subproblem_array[i][c - item.weight] + item.value \
                    >= subproblem_array[i][c]:
                best_items.add(i + 1)
                c -= item.weight

    return best_items


