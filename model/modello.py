from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}

    def buildGraph(self, y: int, s: str):
        self._grafo.clear()
        sight = DAO.get_nodes(y, s)
        self._grafo.add_nodes_from(sight)

        for si in sight:
            self._idMap[si.id] = si

        edges = DAO.get_edges(y, s, self._idMap)
        for s1, s2, p in edges:
            self._grafo.add_edge(s1, s2, weight=p)


    def getTopFiveEdges(self):
        listaEdges = sorted(self._grafo.edges(data=True), key=lambda edge: edge[2].get('weight'), reverse=True)
        return listaEdges[0:5]

    def getYear(self):
        return DAO.get_years()

    def getShape(self, y: int):
        return DAO.get_shapes_year(y)

    def getNodes(self):
        return len(self._grafo.nodes)

    def getEdges(self):
        return len(self._grafo.edges)
