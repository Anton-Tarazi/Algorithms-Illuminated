import queue
from abc import ABC, abstractmethod

from part2.chapter10 import MinHeap


class Vertex(ABC):
    def __init__(self, name: int):
        self.name = name
        self.explored = False
        self.distance = float('inf')

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return self.name


class UndirectedVertex(Vertex):
    def __init__(self, name):
        super().__init__(name)
        self.adjacent_edges = []

    def get_edges(self):
        return self.adjacent_edges


class DirectedVertex(Vertex):
    def __init__(self, name):
        super().__init__(name)
        self.outgoing_edges = []
        self.incoming_edges = []

        self.top_order = 0
        self.scc = 0

    def get_edges(self):
        return self.outgoing_edges


class Edge:
    def __init__(self, from_vertex: Vertex, to_vertex: Vertex, weight: int):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight


class UndirectedEdge(Edge):
    def one_vertex_explored(self):
        return (self.from_vertex.explored and not self.to_vertex.explored) or \
               (not self.from_vertex.explored and self.to_vertex.explored)

    def mark_vertices_explored(self):
        self.from_vertex.explored = True
        self.to_vertex.explored = True

    def __str__(self):
        if self.weight != 1:
            return f"{self.weight}: {self.from_vertex.name} <-> {self.to_vertex.name}"
        else:
            return f"{self.from_vertex.name} <-> {self.to_vertex.name}"


class DirectedEdge(Edge):
    def get_vertex(self, from_vertex=False):
        """default returns to_vertex, but if from_vertex is set to true
        returns from_vertex"""
        if from_vertex:
            return self.from_vertex
        else:
            return self.to_vertex

    def __str__(self):
        if self.weight != 1:
            return f"{self.weight}: {self.from_vertex.name} --> {self.to_vertex.name}"
        else:
            return f"{self.from_vertex.name} --> {self.to_vertex.name}"


class Graph(ABC):
    def __init__(self):
        """self.vertices is a dictionary where the keys are the names of each vertex
        (an int) and the values are a vertex object"""
        self.vertices = {}
        self.edges = []

    def add_vertex_by_obj(self, vertex: Vertex):
        """Adds vertex object to self.vertices"""
        self.vertices[vertex.name] = vertex

    @abstractmethod
    def display(self):
        raise NotImplementedError

    def mark_unexplored(self):
        """Marks all vertices as unexplored"""
        for vertex in self.vertices.values():
            vertex.explored = False

    def clear_distances(self):
        """Resets all distances to +inf"""
        for vertex in self.vertices.values():
            vertex.distance = float("inf")

    def bfs(self, starting_vertex_name: int):
        """Returns all vertices reachable from starting vertex"""
        self.mark_unexplored()

        # initialize queue with starting vertex
        starting_vertex = self.vertices[starting_vertex_name]
        starting_vertex.explored = True
        q = queue.Queue()
        q.put(starting_vertex)

        while not q.empty():
            next_vertex = q.get()
            for edge in next_vertex.get_edges():
                if not edge.to_vertex.explored:
                    edge.to_vertex.explored = True
                    q.put(edge.to_vertex)

        # return list of names of discovered vertices
        return [vertex.name for vertex in self.vertices.values() if vertex.explored]

    def augmented_bfs(self, starting_vertex_name: int):
        """Returns distances (in unweighted graph) of all vertices found from
        starting vertex"""
        self.mark_unexplored()
        self.clear_distances()

        starting_vertex = self.vertices[starting_vertex_name]
        starting_vertex.distance = 0
        starting_vertex.explored = True

        q = queue.Queue()
        q.put(starting_vertex)
        while not q.empty():
            next_vertex = q.get()
            for edge in next_vertex.get_edges():
                if not edge.to_vertex.explored:
                    edge.to_vertex.explored = True
                    edge.to_vertex.distance = next_vertex.distance + 1
                    q.put(edge.to_vertex)

        # return dictionary of vertex name: vertex distance
        return {name: vertex.distance for name, vertex in self.vertices.items()}

    def dfs(self, starting_vertex_name: int):
        """Returns all vertices reachable from starting vertex"""
        self.mark_unexplored()
        starting_vertex = self.vertices[starting_vertex_name]
        self.recursive_dfs(starting_vertex)

        # returns list of all vertex names that have been discovered from starting vertex
        return [vertex.name for vertex in self.vertices.values() if vertex.explored]

    def recursive_dfs(self, starting_vertex: DirectedVertex | UndirectedVertex):
        starting_vertex.explored = True

        for edge in starting_vertex.get_edges():
            if not edge.to_vertex.explored:
                self.recursive_dfs(edge.to_vertex)


class UndirectedGraph(Graph):

    def add_vertex_by_name(self, name: int):
        """Adds new vertex object to graph given vertex name"""
        new_vertex = UndirectedVertex(name)
        self.add_vertex_by_obj(new_vertex)

    def add_edge_by_name(self, from_vertex_name: int, to_vertex_name: int, weight: int = 1):
        """Adds new edge to graph. Edge is added to adjacency lists of both vertices.
        If the vertices aren't in the graph they will be added"""
        if self.vertices.get(from_vertex_name) is None:
            self.add_vertex_by_name(from_vertex_name)
        if self.vertices.get(to_vertex_name) is None:
            self.add_vertex_by_name(to_vertex_name)

        from_vertex = self.vertices[from_vertex_name]
        to_vertex = self.vertices[to_vertex_name]

        # adds edge to adjacent_edges list of both from_vertex and to_vertex
        forward_edge = UndirectedEdge(from_vertex, to_vertex, weight)
        from_vertex.adjacent_edges.append(forward_edge)

        backward_edge = UndirectedEdge(to_vertex, from_vertex, weight)
        to_vertex.adjacent_edges.append(backward_edge)

        # only need to add one copy of edge to self.edges
        self.edges.append(forward_edge)

    def display(self):
        """Print out the graph"""
        for name, vertex in sorted(self.vertices.items()):
            print(f"vertex: {name}, adjacent edges: "
                  f"{[str(adjacent_edge) for adjacent_edge in vertex.adjacent_edges]}")

    def connected_components(self):
        """Returns a list of lists where each sublist represents a connected component
        and contains a list of the names of all vertices in the component"""
        self.mark_unexplored()

        components_list = []

        # loop through all vertices
        for vertex in self.vertices.values():
            if not vertex.explored:
                # for unexplored vertices add a new sublist to components list
                # and do bfs
                vertex.explored = True
                components_list.append([])

                q = queue.Queue()
                q.put(vertex)

                while not q.empty():
                    next_vertex = q.get()
                    components_list[-1].append(next_vertex.name)
                    for edge in next_vertex.get_edges():
                        if not edge.to_vertex.explored:
                            edge.to_vertex.explored = True
                            q.put(edge.to_vertex)
        # returns list of lists of vertex names, where each sublist contains
        # all the vertices in one connected component
        return components_list


class DirectedGraph(Graph):

    def add_vertex_by_name(self, name: int):
        """Adds a new vertex object to the graph given vertex name"""
        new_vertex = DirectedVertex(name)
        self.add_vertex_by_obj(new_vertex)

    def add_edge_by_name(self, from_vertex_name: int, to_vertex_name: int, weight: int = 1):
        """Adds new edge to graph. Edge is added to outgoing list of from_vertex and
        incoming list of to vertex. If the vertices aren't in the graph they will be added"""
        if self.vertices.get(from_vertex_name) is None:
            self.vertices[from_vertex_name] = DirectedVertex(from_vertex_name)
        if self.vertices.get(to_vertex_name) is None:
            self.vertices[to_vertex_name] = DirectedVertex(to_vertex_name)

        from_vertex = self.vertices[from_vertex_name]
        to_vertex = self.vertices[to_vertex_name]

        # adds edge to outgoing of from_vertex and incoming of to_vertex
        new_edge = DirectedEdge(from_vertex, to_vertex, weight)
        from_vertex.outgoing_edges.append(new_edge)
        to_vertex.incoming_edges.append(new_edge)

        self.edges.append(new_edge)

    def display(self):
        """Print out the graph"""
        for name, vertex in sorted(self.vertices.items()):
            print(f"vertex: {name}, outgoing edges: "
                  f"{[str(outgoing_edge) for outgoing_edge in vertex.outgoing_edges]}")

    def topo_sort(self, reverse=False, return_names=True):
        """Topological ordering of DAG. If reverse is set to true, computes topological
        ordering of reversed graph where all edges face opposite direction. Default is to return
        a dictionary of vertex_name: vertex_top_order but if return_names is set to false,
        returns a list of vertex objects ordered from highest to lowest topological ordering."""
        self.mark_unexplored()
        for vertex in self.vertices.values():
            vertex.top_order = 0

        ordered_vertices = []

        current_label = len(self.vertices)
        for vertex in self.vertices.values():
            if not vertex.explored:
                # call dfs for each new vertex
                ordered_vertices, current_label = \
                    self.dfs_topo(vertex, current_label, ordered_vertices, reverse)

        if return_names:
            return {vertex.name: vertex.top_order for vertex in ordered_vertices}
        else:
            return ordered_vertices

    def dfs_topo(self, vertex: DirectedVertex, current_label: int, vertex_array: list, rev: bool):
        """Helper function for topo_sort. Basically dfs but with extra bookkeeping. Reversed is
        default False in topo_sort, so rev is False. False rev makes dfs work on to_vertex in
        outgoing_edges but True rev makes dfs work on from_vertex in incoming_edges"""
        vertex.explored = True

        edges_to_check = vertex.outgoing_edges if not rev else vertex.incoming_edges
        for edge in edges_to_check:
            if not edge.get_vertex(rev).explored:
                vertex_array, current_label = \
                    self.dfs_topo(edge.get_vertex(rev), current_label, vertex_array, rev)

        vertex.top_order = current_label
        vertex_array.append(vertex)
        current_label -= 1
        return vertex_array, current_label

    def strong_connected_components(self, return_list=False):
        """Kosaraju algorithm. Computes strongly connected components right directed graph.
        Returns list of sizes of connected components"""

        # sort vertices in reverse topological order
        vertices_in_top_order = self.topo_sort(reverse=True, return_names=False)
        self.mark_unexplored()

        strong_ccs = []
        num_scc = 0
        # iterate through all in reverse topological order
        for vertex in vertices_in_top_order[::-1]:
            # call dfs on every unexplored vertex
            if not vertex.explored:
                num_scc += 1
                strong_ccs.append([])
                strong_ccs = self.dfs_scc(vertex, num_scc, strong_ccs)

        # return either a list of ccs or just a list of their lengths depending
        # on need
        if return_list:
            return strong_ccs
        else:
            return [len(connected_component) for connected_component in strong_ccs]

    def dfs_scc(self, vertex: DirectedVertex, num_scc: int, scc_list: list):
        """Helper dfs for Kosaraju algorithm. Works the same way but with some extra
        bookkeeping"""
        vertex.explored = True
        vertex.scc = num_scc
        scc_list[-1].append(vertex)
        for edge in vertex.outgoing_edges:
            if not edge.to_vertex.explored:
                self.dfs_scc(edge.to_vertex, num_scc, scc_list)

        # returns list of lists where each sublist is the vertex objects of a scc
        return scc_list

    def dijkstra(self, starting_vertex_name):
        """Dijkstra's algorithm inefficient version. Returns dictionary of all vertices
        and their min distance from the starting vertex"""
        self.mark_unexplored()
        self.clear_distances()

        starting_vertex = self.vertices[starting_vertex_name]
        starting_vertex.distance = 0

        # initialize list of unexplored vertices
        unexplored_vertices = [starting_vertex]

        while len(unexplored_vertices) != 0:
            # make the current vertex the one with the smallest distance and
            # mark as explored
            current_vertex = min(unexplored_vertices, key=lambda vertex: vertex.distance)
            current_vertex.explored = True

            # delete current vertex from unexplored vertices
            unexplored_vertices = \
                [vertex for vertex in unexplored_vertices if vertex != current_vertex]

            # loop through all edges of current vertex that lead to
            # unexplored vertices
            for edge in current_vertex.outgoing_edges:
                if not edge.to_vertex.explored:
                    unexplored_vertices.append(edge.to_vertex)
                    # if distance through the current vertex is less than old
                    # distance, update distance with smaller value
                    if current_vertex.distance + edge.weight < edge.to_vertex.distance:
                        edge.to_vertex.distance = current_vertex.distance + edge.weight

        return {vertex.name: vertex.distance for vertex in self.vertices.values()}

    def dijkstra_2(self, starting_vertex_name):
        """A second implementation of Dijkstra's algorithm, also inefficient. This version
        is more similar to the pseudocode in the book. Returns dictionary of all vertices
        and their min distance from the starting vertex"""

        # initialize explored vertices to just starting vertex and set its
        # distance to 0, all other distances are +inf
        self.mark_unexplored()
        self.clear_distances()
        starting_vertex = self.vertices[starting_vertex_name]
        starting_vertex.distance = 0
        starting_vertex.explored = True

        # run loop as long as there is an unexplored vertex
        while True:

            # find the edge that minimizes the Dijkstra score
            # ie the edge such that the distance of its from_vertex
            # plus its weight is smallest
            min_dist = float("inf")
            min_edge = None
            for edge in self.edges:
                if edge.from_vertex.explored and not edge.to_vertex.explored:

                    if edge.from_vertex.distance + edge.weight < min_dist:
                        min_edge = edge
                        min_dist = edge.from_vertex.distance + edge.weight

            # if no edge replaces min edge then we must have exhausted
            # all reachable vertices so break out of main while loop
            if min_edge is None:
                break

            # set the distance of the to_vertex of the minimum edge to
            # this minimum value and mark the vertex as explored
            min_edge.to_vertex.explored = True
            min_edge.to_vertex.distance = min_dist

        return {vertex.name: vertex.distance for vertex in self.vertices.values()}

    def efficient_dijkstra(self, starting_vertex_name: int):
        """Dijkstra's algorithm making use of a priority queue. Returns a dictionary of all
        vertices and their distance from the starting vertex"""

        self.clear_distances()
        starting_vertex = self.vertices[starting_vertex_name]
        starting_vertex.distance = 0

        # initialize a priority queue with all vertices and loop until queue is empty
        priority_q = MinHeap(array=list(self.vertices.values()), key=lambda v: v.distance)

        while not priority_q.is_empty():

            # get the vertex that is closest to source
            current_vertex = priority_q.extract_min()

            # for each edge in this vertex, if its path through this vertex is less
            # than its current path, update path to this shorter one
            for edge in current_vertex.outgoing_edges:
                if current_vertex.distance + edge.weight < edge.to_vertex.distance:

                    # delete vertex from queue
                    to_vertex_index = priority_q.positions[edge.to_vertex]
                    priority_q.delete_by_index(to_vertex_index)
                    # change vertex distance and reinsert in queue
                    edge.to_vertex.distance = current_vertex.distance + edge.weight
                    priority_q.add(edge.to_vertex)

        return {vertex.name: vertex.distance for vertex in self.vertices.values()}
