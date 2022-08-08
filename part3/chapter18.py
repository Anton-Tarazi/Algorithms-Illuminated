from part2.chapter9 import DirectedGraph


class NegativeEdgeGraph(DirectedGraph):

    def __init__(self):
        super().__init__()

    def bellman_ford(self, starting_vertex_name):
        """Bellman-Ford Algorithm for finding the shortest paths in a graph with negative edge weights.
        This implementation is true to the pseudocode in the book, where on each inner loop
        we iterate through all vertices and then iterate through all incoming edges of each vertex.
        O(mn) runtime"""

        n = len(self.vertices)
        subproblems = [[float('inf') for _ in range(n)] for _ in range(n + 1)]
        subproblems[0][starting_vertex_name - 1] = 0

        for i in range(1, n + 1):
            stable = True

            for name, vertex in self.vertices.items():
                new_distance = float('inf')
                for edge in vertex.incoming_edges:
                    new_distance = \
                        min(new_distance, subproblems[i - 1][edge.from_vertex.name - 1] + edge.weight)
                subproblems[i][name - 1] = min(subproblems[i - 1][name - 1], new_distance)
                if subproblems[i][name - 1] != subproblems[i - 1][name - 1]:
                    stable = False

            if stable:
                return subproblems[i - 1]
        return "NEGATIVE CYCLE"

    def clean_bellman_ford(self, starting_vertex_name):
        """A slightly cleaner version of the Bellman-Ford algorthm. Instead of iterating through all
        vertices in each inner loop, we iterate through all edges and directly modify the distance
        of the to_vertex of the edge based on the edge length and the from_vertex distance. Another
        small change is switching the dynamic programming array to be 1D instead of 2D and the
        elimination of the stable boolean. Also has  O(mn) runtime"""

        n = len(self.vertices)
        subproblems = [float('inf') for _ in range(n)]
        subproblems[starting_vertex_name - 1] = 0

        for i in range(1, n + 1):
            current_sub = subproblems[:]

            for edge in self.edges:
                w = edge.from_vertex
                v = edge.to_vertex

                current_sub[v.name - 1] = \
                    min(current_sub[v.name - 1], subproblems[w.name - 1] + edge.weight)

            if current_sub == subproblems:
                return current_sub
            subproblems = current_sub
        return "NEGATIVE CYCLE"

    def floyd_marshall(self):
        """Floyd-Marshall all pairs shortest-paths algorithm. O(n^3) runtime"""

        n = len(self.vertices)
        subproblems = [[float('inf') for _ in range(n)] for _ in range(n)]

        for v_name, vertex in self.vertices.items():
            subproblems[v_name - 1][v_name - 1] = 0
            for edge in vertex.outgoing_edges:
                subproblems[v_name - 1][edge.to_vertex.name - 1] = edge.weight

        for k in range(n):
            sub_copy = [row[:] for row in subproblems]
            for v in range(n):
                for w in range(n):
                    sub_copy[v][w] = min(sub_copy[v][w], subproblems[v][k] + subproblems[k][w])

            subproblems = sub_copy

        for v in range(n):
            if subproblems[v][v] < 0:
                return "NEGATIVE CYCLE"

        return subproblems
