from part2.chapter9 import DirectedGraph, UndirectedGraph
from part3.chapter13 import Job


# A collection of functions that generate data structures from text files.
# Used to get the test cases from https://algorithmsilluminated.org/ to check
# the validity of my implementations.


def create_list(filename: str) -> list[int]:
    output_list = []
    with open(filename, "r") as file:
        for line in file:
            output_list.append(int(line.rstrip()))
    return output_list


def create_directed_graph(filename: str) -> DirectedGraph:
    pass


def create_dijkstra_graph(filename: str) -> DirectedGraph:
    pass


def create_job_list(filename: str) -> list[Job]:
    pass


# create_list("../test_cases/part1_test_cases/problem3.5test.txt")
# create_list("../test_cases/part2_test_cases/problem11.3test.txt")