import requests

from part2.chapter9 import DirectedGraph
from part3.chapter13 import Job, greedy_difference


def create_list(link):
    link_data = requests.get(link)
    string_list = link_data.text.split(sep="\r\n")[:-1]
    num_list = [int(num) for num in string_list]
    return num_list


def create_list2(link):
    link_data = requests.get(link)
    string_list = link_data.text.split(sep="\n")[:-1]
    num_list = [int(num) for num in string_list]
    return num_list


def create_directed_graph(link):
    link_data = requests.get(link)
    string_list = [string.rstrip() for string in link_data.text.split(sep="\n") if string != ""]
    split_string_list = [string.split(sep=" ") for string in string_list]
    clean_split_string_list = [string for string in split_string_list if string != ""]
    list_of_num_list = [[int(x) for x in small_list] for small_list in clean_split_string_list]

    new_graph = DirectedGraph()
    for tup in list_of_num_list:
        new_graph.add_edge_by_name(tup[0], tup[1])
    return new_graph


def create_dijkstra_graph(link):
    txt_data = requests.get(link)
    separated_entries = [string for string in txt_data.text.split(sep="\n") if string != ""]

    new_graph = DirectedGraph()
    for entry in separated_entries:
        entry_list = [string for string in entry.split(sep="\t") if string != "\r"]

        from_vertex = int(entry_list[0])
        str_to_vertices_and_weights = [vw_pair.split(sep=",") for vw_pair in entry_list[1:]]
        int_to_vertices_and_weights = \
            [[int(x) for x in pair] for pair in str_to_vertices_and_weights]

        for vw_pair in int_to_vertices_and_weights:
            to_vertex = vw_pair[0]
            weight = vw_pair[1]
            new_graph.add_edge_by_name(from_vertex, to_vertex, weight)
    return new_graph


def create_jobs(filepath):
    with open(filepath, "r") as file:
        text = file.read()
    raw_data = text.split("\n")[8:-1]
    no_slashes = [string[:-1] for string in raw_data]
    string_data = [string.split(sep=" ") for string in no_slashes]
    num_data = [[int(string) for string in small_list] for small_list in string_data]
    return [Job(entry[0], entry[1]) for entry in num_data]


count_inv_test1 = create_list("https://algorithmsilluminated.org/datasets/problem3.5test.txt")
count_inv_test2 = create_list("https://algorithmsilluminated.org/datasets/problem3.5.txt")

quicksort_test1 = create_list("https://algorithmsilluminated.org/datasets/problem5.6test1.txt")
quicksort_test2 = create_list("https://algorithmsilluminated.org/datasets/problem5.6test2.txt")
quicksort_test3 = create_list("https://algorithmsilluminated.org/datasets/problem5.6.txt")

select_test1 = create_list("https://algorithmsilluminated.org/datasets/problem6.5test1.txt")
select_test2 = create_list("https://algorithmsilluminated.org/datasets/problem6.5test2.txt")

scc_test1 = create_directed_graph("https://algorithmsilluminated.org/datasets/problem8.10test1.txt")
scc_test2 = create_directed_graph("https://algorithmsilluminated.org/datasets/problem8.10test2.txt")
scc_test3 = create_directed_graph("https://algorithmsilluminated.org/datasets/problem8.10test3.txt")
scc_test4 = create_directed_graph("https://algorithmsilluminated.org/datasets/problem8.10test4.txt")
scc_test5 = create_directed_graph("https://algorithmsilluminated.org/datasets/problem8.10test5.txt")

dijkstra_test1 = create_dijkstra_graph("https://algorithmsilluminated.org/datasets/problem9.8test.txt")
dijkstra_test2 = create_dijkstra_graph("https://algorithmsilluminated.org/datasets/problem9.8.txt")

med_main_test1 = create_list2("https://algorithmsilluminated.org/datasets/problem11.3test.txt")
med_main_test2 = create_list2("https://algorithmsilluminated.org/datasets/problem11.3.txt")

two_sum_test1 = create_list2("https://algorithmsilluminated.org/datasets/problem12.4test.txt")

