import heapq
import sys

##CARGAR ARCHIVOS TXT
def cargarArchivo(nombre_archivo, dirigido=False):
    with open(nombre_archivo, 'r') as f:
        lines = f.readlines()
    edges = []
    vertices = set()
    graph = {}
    for line in lines:
        u, v, w = map(int, line.strip().split(','))
        edges.append((u, v, w))
        vertices.update([u, v])
        if u not in graph:
            graph[u] = {}
        if not dirigido:
            if v not in graph:
                graph[v] = {}
        graph[u][v] = w
        if not dirigido:
            graph[v][u] = w
    return edges, max(vertices), graph

##Guardar Archivo
def guardarArchivo(nombre_archivo, resultado):
    with open(nombre_archivo, 'w') as f:
        for u, v, w in resultado:
            f.write(f"{u},{v},{w}\n")

##Algoritmo Kruskal
class Kruskal:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal_mst(self):
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = [i for i in range(self.V + 1)]
        rank = [0] * (self.V + 1)

        while e < self.V - 1:
            u, v, w = self.graph[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            if x != y:
                e += 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)

        return result

def prim(graph, start=1):
    mst = []
    visited = set([start])
    edges = [(weight, start, v) for v, weight in graph[start].items()]
    heapq.heapify(edges)

    while edges:
        weight, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            mst.append((u, v, weight))
            for next_v, next_weight in graph[v].items():
                if next_v not in visited:
                    heapq.heappush(edges, (next_weight, v, next_v))

    return mst

##Algoritmo Dijkstra
class Dijkstra:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices + 1)]

    def add_edge(self, u, v, w):
        self.graph[u].append((w, v))

    def dijkstra(self, src):
        dist = [float('inf')] * (self.V + 1)
        dist[src] = 0
        pq = [(0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for w, v in self.graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        return dist

##Definir los grafos
def main():
    grafos = [
        ('kruskal', 'Grafo50.txt', 'resul_Kruskal.txt', False),
        ('prim', 'Grafo50.txt', 'resul_Prim.txt', False),
        ('dijkstra', 'Grafo30.txt', 'resul_Dijkstra.txt', True)
    ]

    for alg, archivoE, archivoS, dirigido in grafos:
        edges, vertices, graph = cargarArchivo(archivoE, dirigido)

        if alg == 'kruskal':
            g = Kruskal(vertices)
            for u, v, w in edges:
                g.add_edge(u, v, w)
            resultado = g.kruskal_mst()
        elif alg == 'prim':
            resultado = prim(graph)
        elif alg == 'dijkstra':
            nodo_origen = 1  # Cambiar al nodo de origen deseado
            g = Dijkstra(vertices)
            for u, v, w in edges:
                g.add_edge(u, v, w)
            d = g.dijkstra(nodo_origen)
            resultado = [(nodo_origen, i, d[i]) for i in range(1, vertices + 1) if d[i] != float('inf')]
        else:
            print("Incorrecto")
            sys.exit(1)

        guardarArchivo(archivoS, resultado)

if __name__ == "__main__":
    main()