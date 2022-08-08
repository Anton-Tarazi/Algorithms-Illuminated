from part2.chapter9 import DirectedGraph
from part3.chapter13 import Job
from part3.chapter14 import HuffNode
from part3.chapter15 import MSTGraph
from part3.chapter16 import KnapsackItem
from part3.chapter18 import NegativeEdgeGraph

# A collection of functions that generate data structures from text files.
# Used to get the test cases from https://algorithmsilluminated.org/ to verify
# my implementations.


def create_list(filename: str) -> list[int]:
    output_list = []
    with open(filename, "r") as file:
        for line in file:
            output_list.append(int(line.rstrip()))
        return output_list


def create_special_graph(graph, filename: str):
    with open(filename, "r") as file:
        for line in file:
            edge_data = line.rstrip().split(sep=" ")
            vertex_1 = int(edge_data[0])
            vertex_2 = int(edge_data[1])
            weight = int(edge_data[2])
            graph.add_edge_by_name(vertex_1, vertex_2, weight)


def create_mst_graph(filename: str) -> MSTGraph:
    new_graph = MSTGraph()
    create_special_graph(new_graph, filename)
    return new_graph


def create_negative_edge_graph(filename: str) -> NegativeEdgeGraph:
    new_graph = NegativeEdgeGraph()
    create_special_graph(new_graph, filename)
    return new_graph


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


def create_alphabet(filename: str) -> list[HuffNode]:
    alphabet = []
    with open(filename, "r") as file:
        for index, line in enumerate(file):
            frequency = int(line.rstrip())
            new_symbol = HuffNode(str(index), frequency)
            alphabet.append(new_symbol)
        return alphabet


def create_knapsack_item_list(filename: str) -> list[KnapsackItem]:
    items = []
    with open(filename, "r") as file:
        for line in file:
            value_weight_list = line.rstrip().split(sep=" ")
            value = int(value_weight_list[0])
            weight = int(value_weight_list[1])
            new_item = KnapsackItem(value, weight)
            items.append(new_item)
        return items


def create_sequences(filename: str) -> tuple:
    sequences = []
    with open(filename, "r") as file:
        for line in file:
            sequences.append(line.rstrip())
        return tuple(sequences)


def create_frequencies(filename: str) -> list[int]:
    with open(filename, "r") as file:
        frequencies_strs = file.readline().rstrip().split(sep=",")
        return [int(x) for x in frequencies_strs]
