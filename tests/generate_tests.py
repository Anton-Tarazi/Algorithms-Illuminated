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
    new_graph = DirectedGraph()
    with open(filename,  "r") as file:
        for line in file:
            edge = line.rstrip().split(sep=" ")
            vertex_1 = int(edge[0])
            vertex_2 = int(edge[1])
            new_graph.add_edge_by_name(vertex_1, vertex_2)
        return new_graph


def create_dijkstra_graph(filename: str) -> DirectedGraph:
    new_graph = DirectedGraph()
    with open(filename, "r") as file:
        for line in file:
            vertex_and_connections = line.rstrip().split(sep="\t")
            from_vertex = int(vertex_and_connections[0])

            for vertex_weight_pair in vertex_and_connections[1:]:
                separated_pair = vertex_weight_pair.split(sep=",")
                to_vertex = int(separated_pair[0])
                weight = int(separated_pair[1])

                new_graph.add_edge_by_name(from_vertex, to_vertex, weight)
        return new_graph


def create_job_list(filename: str) -> list[Job]:
    job_list = []
    with open(filename, "r") as file:
        for line in file:
            weight_length_list = line.rstrip().split(sep=" ")
            weight = int(weight_length_list[0])
            length = int(weight_length_list[1])

            new_job = Job(weight, length)
            job_list.append(new_job)
        return job_list



