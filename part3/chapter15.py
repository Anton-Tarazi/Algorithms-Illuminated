import random

from part2.chapter9 import UndirectedVertex, UndirectedEdge, UndirectedGraph
from part2.chapter10 import MinHeap


class MSTVertex(UndirectedVertex):

    def __init__(self, name):
        super().__init__(name)
        self.key = float('inf')

        # prim initialization
        self.prim_winner = None

        # union find initialization
        self.parent = self
        self.size = 1


class MSTGraph(UndirectedGraph):

    def __init__(self, graph=None):
        super().__init__()

        # can pass a graph into the initialization to create a copy
        # of all the vertices
        if graph is not None:
            for vertex_name in graph.vertices.keys():
                copy_vertex = MSTVertex(vertex_name)
                self.add_vertex_by_obj(copy_vertex)

    def add_vertex_by_name(self, name: int):
        """Adds new vertex object to graph given vertex name"""
        new_vertex = MSTVertex(name)
        self.add_vertex_by_obj(new_vertex)

    def clear_prim_winners(self):
        for vertex in self.vertices.values():
            vertex.prim_winner = None

    def prim(self):
        """Inefficient version of prims algorithm. Returns a minimum spanning tree
        in O(mn) runtime"""
        self.mark_unexplored()
        starting_vertex = random.choice(list(self.vertices.values()))
        starting_vertex.explored = True

        spanning_tree = MSTGraph(self)

        while True:
            min_weight = float('inf')
            min_edge = None

            # loop over all edges extending from explored vertices to unexplored vertices
            # and find the one with minimum weight
            for edge in self.edges:
                if edge.one_vertex_explored():
                    if edge.weight < min_weight:
                        min_edge = edge
                        min_weight = edge.weight

            # if the min_edge stays as None, it means that there are no more edges
            # extending the boundary, so we are done
            if min_edge is None:
                break
            # add the minimum edge to the spanning tree
            else:
                min_edge.mark_vertices_explored()
                spanning_tree.add_edge(min_edge)
        return spanning_tree

    def efficient_prim(self):
        """Efficient version of prims algorithm Returns the minimum spanning tree
        in O(m log n) runtime"""

        # choose arbitrary starting vertex and initialize spanning tree
        starting_vertex = random.choice(list(self.vertices.values()))
        spanning_tree = MSTGraph(self)

        self.clear_distances()
        self.mark_unexplored()
        self.clear_prim_winners()

        # initialize the key of each vertex adjacent to s to be the weight of the connecting
        # edge and the winning edge to be that edge. All other vertices to have a key of +inf
        # and no winning edge
        for edge in starting_vertex.adjacent_edges:
            adjacent_vertex = edge.to_vertex

            adjacent_vertex.prim_winner = edge
            adjacent_vertex.key = edge.weight

        # initialize a priority queue of all vertices except starting vertex
        starting_vertex.key = -float('inf')
        priority_q = MinHeap(array=list(self.vertices.values()), key=lambda v: v.key)
        priority_q.extract_min()

        # loop until all vertices are added to the spanning tree
        while not priority_q.is_empty():

            # get the unexplored vertex that has the smallest connecting
            # edge to the tree so far
            current_vertex = priority_q.extract_min()
            current_vertex.explored = True
            current_edge = current_vertex.prim_winner

            spanning_tree.add_edge(current_edge)

            #  update the keys and winning edges of all vertices unexplored vertices adjacent to
            # the vertex just processed
            for edge in current_vertex.adjacent_edges:
                if not edge.to_vertex.explored:
                    if edge.weight < edge.to_vertex.key:
                        # delete vertex from queue
                        to_vertex_index = priority_q.positions[edge.to_vertex]
                        priority_q.delete_by_index(to_vertex_index)
                        # change vertex distance and reinsert in queue
                        edge.to_vertex.key = edge.weight
                        edge.to_vertex.prim_winner = edge
                        priority_q.add(edge.to_vertex)

        return spanning_tree

    def kruskal(self):
        """Straightforward implementation of kruskals algorithm. O(mn) runtime"""
        spanning_tree = MSTGraph(self)

        # sort the edges and iterate from lowest to highest weight, adding an edge
        # to the spanning tree the endpoints do not already contain a path
        sorted_edges = sorted(self.edges, key=lambda e: e.weight)
        for edge in sorted_edges:
            if not spanning_tree.has_path(edge.from_vertex.name, edge.to_vertex.name):
                spanning_tree.add_edge(edge)

        return spanning_tree

    def efficient_kruskal(self):
        """Union find implementation of kruskals algorithm. O((m+n)log n) runtime"""
        spanning_tree = MSTGraph(self)
        sorted_edges = sorted(self.edges, key=lambda e: e.weight)
        edges_added = 0
        for edge in sorted_edges:
            # if the edpoints of the edge aren't in the same set, add the
            # edge to the spanning tree and merge union the two sets
            if self.find(edge.to_vertex) != self.find(edge.from_vertex):
                spanning_tree.add_edge(edge)

                self.union(edge.to_vertex, edge.from_vertex)

                # when n - 1 edges have been added we can break out of the loop
                edges_added += 1
                if edges_added >= len(self.vertices) - 1:
                    break

        return spanning_tree

    def find(self, vertex: MSTVertex):
        """Returns the name of the set that contains the vertex. O(log n) runtime"""
        if vertex.parent == vertex:
            return vertex
        else:
            return self.find(vertex.parent)

    def union(self, vertex1: MSTVertex, vertex2: MSTVertex):
        """Merge the sets that contain the two vertices. O(log n) runtime."""

        # get references names of sets of each vertex
        vertex1_parent = self.find(vertex1)
        vertex2_parent = self.find(vertex2)

        # if the vertices are in the same set, return
        if vertex1_parent == vertex2_parent:
            return

        # set the parent of the smaller set to be the parent of the
        # larger set
        if vertex1_parent.size >= vertex2_parent.size:
            vertex2_parent.parent = vertex1_parent
            vertex1_parent.size += vertex2_parent.size
        else:
            vertex1_parent.parent = vertex2_parent
            vertex2_parent.size += vertex1_parent.size

    def add_edge(self, edge: UndirectedEdge):
        """Adds an equivalent version of an edge from the parent graph to the
        spanning tree. Note that this version of add_edge only works if the
        endpoints of the edge are already in the graph"""
        spanning_tree_from_vertex = self.vertices[edge.from_vertex.name]
        spanning_tree_to_vertex = self.vertices[edge.to_vertex.name]

        new_forward_edge = \
            UndirectedEdge(spanning_tree_from_vertex, spanning_tree_to_vertex, edge.weight)
        spanning_tree_from_vertex.adjacent_edges.append(new_forward_edge)

        new_backward_edge = \
            UndirectedEdge(spanning_tree_to_vertex, spanning_tree_from_vertex, edge.weight)
        spanning_tree_to_vertex.adjacent_edges.append(new_backward_edge)

        self.edges.append(new_forward_edge)

    def size(self) -> int:
        """Returns sum of all edge weights in spanning tree"""
        return sum(edge.weight for edge in self.edges)

    def has_path(self, vertex1_name: int, vertex2_name: int) -> bool:
        return vertex2_name in self.dfs(vertex1_name)
