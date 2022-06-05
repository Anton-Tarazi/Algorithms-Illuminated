import queue


# Initial attempt at chapter 8. More refined versions of all classes and methods
# are in chapter9.py


class Vertex:

    def __init__(self, name):
        self.name = name
        self.adjacent_vertices = []
        self.explored = False
        self.distance = float('inf')
        self.top_order = 0
        self.scc = 0


class Graph:

    def __init__(self, directed=False):
        self.vertices = {}
        self.reversed_vertices = {}
        self.directed = directed
        self.size = 0
        self.numSCC = 0

    def add_vertex(self, new_vertex):
        self.vertices[new_vertex] = []
        self.reversed_vertices[new_vertex] = []
        self.size += 1

    def add_edge(self, vertex1, vertex2):
        if vertex1 != vertex2:
            self.vertices[vertex1].append(vertex2)
            if self.directed:
                self.reversed_vertices[vertex2].append(vertex1)
            else:
                self.vertices[vertex2].append(vertex1)

    def display(self, reversed=False):
        if reversed:
            return [[vertex.name, [v.name for v in self.reversed_vertices[vertex]]] for vertex in
                    self.reversed_vertices]
        else:
            return [[vertex.name, [v.name for v in self.vertices[vertex]]] for vertex in self.vertices]

    def bfs(self, source_vertex):
        for vertex in self.vertices:
            vertex.explored = False
        source_vertex.explored = True

        discovered_vertices = [source_vertex.name]
        q = queue.Queue()
        q.put(source_vertex)

        while not q.empty():
            v = q.get()
            for vertex in self.vertices[v]:
                if not vertex.explored:
                    vertex.explored = True
                    discovered_vertices.append(vertex.name)
                    q.put(vertex)

        return discovered_vertices

    def augmented_bfs(self, source_vertex):
        for vertex in self.vertices:
            vertex.explored = False
        source_vertex.explored = True

        source_vertex._distance = 0
        min_distances = [{source_vertex.name: source_vertex._distance}]

        q = queue.Queue()
        q.put(source_vertex)
        while not q.empty():
            v = q.get()
            for vertex in self.vertices[v]:
                if not vertex.explored:
                    vertex.explored = True
                    vertex._distance = v._distance + 1
                    q.put(vertex)
                    min_distances.append({vertex.name: vertex._distance})

        return min_distances

    def ucc(self):
        connected_components = []
        for vertex in self.vertices:
            vertex.explored = False

        for i in self.vertices.keys():
            if not i.explored:
                i.explored = True
                connected_components.append([])
                q = queue.Queue()
                q.put(i)
                while not q.empty():
                    v = q.get()
                    connected_components[-1].append(v.name)
                    for vertex in self.vertices[v]:
                        if not vertex.explored:
                            vertex.explored = True
                            q.put(vertex)

        return connected_components

    def dfs(self, source_vertex, discovered_vertices=None):
        if discovered_vertices is None:
            discovered_vertices = []
        source_vertex.explored = True
        discovered_vertices.append(source_vertex.name)
        for adjacent_vertex in self.vertices[source_vertex]:
            if not adjacent_vertex.explored:
                self.dfs(adjacent_vertex)

        return discovered_vertices

    def toposort(self):
        temp = self.size
        if not self.directed:
            return
        for vertex in self.vertices:
            vertex.explored = False

        for vertex in self.vertices:
            if not vertex.explored:
                self.dfs_topo(vertex)
        self.size = temp
        return [{vertex.name: vertex.top_order} for vertex in self.vertices]

    def dfs_topo(self, source_vertex):
        source_vertex.explored = True
        for adjacent_vertex in self.vertices[source_vertex]:
            if not adjacent_vertex.explored:
                self.dfs_topo(adjacent_vertex)
        source_vertex.top_order = self.size
        self.size -= 1

    def reversed_toposort(self):
        temp = self.size
        if not self.directed:
            return
        for vertex in self.reversed_vertices:
            vertex.explored = False

        for vertex in self.reversed_vertices:
            if not vertex.explored:
                self.reversed_dfs_topo(vertex)
        self.size = temp
        return [{vertex.name: vertex.top_order} for vertex in self.reversed_vertices]

    def reversed_dfs_topo(self, source_vertex):
        source_vertex.explored = True
        for adjacent_vertex in self.reversed_vertices[source_vertex]:
            if not adjacent_vertex.explored:
                self.reversed_dfs_topo(adjacent_vertex)
        source_vertex.top_order = self.size
        self.size -= 1

    def sort_vertices(self):
        return [(vertex.name, vertex.top_order) for vertex in sorted(self.vertices, key=lambda x: x.top_order)]

    def kosaraju(self):
        self.reversed_toposort()
        for vertex in self.vertices:
            vertex.explored = False

        print([vertex.top_order for vertex in sorted(self.vertices, key=lambda x: x.top_order, reverse=False)])
        for vertex in sorted(self.vertices, key=lambda x: x.top_order, reverse=False):
            if not vertex.explored:
                self.numSCC += 1
                self.dfs_scc(vertex)

        return [[vertex.name for vertex in self.vertices if vertex.scc == i]
                for i in range(1, self.numSCC+1)]

    def dfs_scc(self, source_vertex):
        source_vertex.explored = True
        source_vertex.scc = self.numSCC
        for adjacent_vertex in self.vertices[source_vertex]:
            if not adjacent_vertex.explored:
                self.dfs_scc(adjacent_vertex)


practice_graph = Graph(directed=False)
s = Vertex("s")
a = Vertex("a")
b = Vertex("b")
c = Vertex("c")
d = Vertex("d")
e = Vertex("e")
practice_graph.add_vertex(s)
practice_graph.add_vertex(a)
practice_graph.add_vertex(b)
practice_graph.add_vertex(c)
practice_graph.add_vertex(d)
practice_graph.add_vertex(e)

practice_graph.add_edge(s, a)
practice_graph.add_edge(s, b)
practice_graph.add_edge(a, c)
practice_graph.add_edge(b, c)
practice_graph.add_edge(c, d)
practice_graph.add_edge(b, d)
practice_graph.add_edge(c, e)
practice_graph.add_edge(d, e)

ucc_practice = Graph()
vertex1 = Vertex("1")
vertex2 = Vertex("2")
vertex3 = Vertex("3")
vertex4 = Vertex("4")
vertex5 = Vertex("5")
vertex6 = Vertex("6")
vertex7 = Vertex("7")
vertex8 = Vertex("8")
vertex9 = Vertex("9")
vertex10 = Vertex("10")

ucc_practice.add_vertex(vertex1)
ucc_practice.add_vertex(vertex2)
ucc_practice.add_vertex(vertex3)
ucc_practice.add_vertex(vertex4)
ucc_practice.add_vertex(vertex5)
ucc_practice.add_vertex(vertex6)
ucc_practice.add_vertex(vertex7)
ucc_practice.add_vertex(vertex8)
ucc_practice.add_vertex(vertex9)
ucc_practice.add_vertex(vertex10)

ucc_practice.add_edge(vertex1, vertex3)
ucc_practice.add_edge(vertex1, vertex5)
ucc_practice.add_edge(vertex3, vertex5)
ucc_practice.add_edge(vertex5, vertex7)
ucc_practice.add_edge(vertex5, vertex9)

ucc_practice.add_edge(vertex2, vertex4)

ucc_practice.add_edge(vertex8, vertex6)
ucc_practice.add_edge(vertex6, vertex10)


topological_practice = Graph(directed=True)
top_s = Vertex("s")
top_v = Vertex("v")
top_w = Vertex("w")
top_t = Vertex("t")

topological_practice.add_vertex(top_s)
topological_practice.add_vertex(top_v)
topological_practice.add_vertex(top_w)
topological_practice.add_vertex(top_t)
topological_practice.add_edge(top_s, top_v)
topological_practice.add_edge(top_s, top_w)
topological_practice.add_edge(top_v, top_t)
topological_practice.add_edge(top_w, top_t)

kosaraju_practice = Graph(directed=True)
v1 = Vertex(1)
v2 = Vertex(2)
v3 = Vertex(3)
v4 = Vertex(4)
v5 = Vertex(5)
v6 = Vertex(6)
v7 = Vertex(7)
v8 = Vertex(8)
v9 = Vertex(9)
v10 = Vertex(10)
v11 = Vertex(11)

kosaraju_practice.add_vertex(v1)
kosaraju_practice.add_vertex(v2)
kosaraju_practice.add_vertex(v3)
kosaraju_practice.add_vertex(v4)
kosaraju_practice.add_vertex(v5)
kosaraju_practice.add_vertex(v6)
kosaraju_practice.add_vertex(v7)
kosaraju_practice.add_vertex(v8)
kosaraju_practice.add_vertex(v9)
kosaraju_practice.add_vertex(v10)
kosaraju_practice.add_vertex(v11)


kosaraju_practice.add_edge(v1, v3)
kosaraju_practice.add_edge(v3, v5)
kosaraju_practice.add_edge(v5, v1)
kosaraju_practice.add_edge(v3, v11)
kosaraju_practice.add_edge(v5, v7)
kosaraju_practice.add_edge(v5, v9)
kosaraju_practice.add_edge(v11, v6)
kosaraju_practice.add_edge(v11, v8)
kosaraju_practice.add_edge(v8, v6)
kosaraju_practice.add_edge(v6, v10)
kosaraju_practice.add_edge(v10, v8)
kosaraju_practice.add_edge(v7, v9)
kosaraju_practice.add_edge(v9, v4)
kosaraju_practice.add_edge(v4, v7)
kosaraju_practice.add_edge(v9, v2)
kosaraju_practice.add_edge(v2, v4)
kosaraju_practice.add_edge(v9, v8)
kosaraju_practice.add_edge(v2, v10)

print(kosaraju_practice.kosaraju())