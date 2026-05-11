import networkx as nx
from networkx import dfs_tree
from networkx.algorithms.shortest_paths.weighted import dijkstra_path
from networkx.algorithms.traversal import bfs_tree

from database.DAO import DAO


class Model:
    def __init__(self):
        self._g = nx.Graph()
        self._idAirports = dict()

    def createGraph(self, n):
        self._g.clear()
        self._g.clear_edges()
        self._idAirports.clear()

        print("Nodi: ", self.sizeNodes())
        for a in DAO.getAirportsN(n):
            self._idAirports[a.ID] = a
            self._g.add_node(a)
        print("Nodi: ", self.sizeNodes())
        print("Archi: ", self.sizeEdges())
        voli = DAO.getFlights()
        for volo in voli:
            u = self._idAirports.get(volo[0], None)
            v = self._idAirports.get(volo[1], None)
            w = volo[2]

            if u is not None and v is not None:
                if self._g.has_edge(u, v):
                    self._g[u][v]['weight'] += w
                else:
                    self._g.add_edge(u, v, weight=w)
        print("Archi: ", self.sizeEdges())
        return self._g.nodes()

    def aeroportiConnessi(self, p):
        tree = dfs_tree(self._g, p)
        return tree.nodes()

    def trovaPercorso(self, p, a):
        path = dijkstra_path(self._g, p, a)

    def sizeNodes(self):
        return len(self._g.nodes())

    def sizeEdges(self):
        return len(self._g.edges())