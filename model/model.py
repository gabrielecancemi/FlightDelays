import copy

import networkx as nx
from networkx import dfs_tree, NetworkXNoPath
from networkx.algorithms.shortest_paths.weighted import dijkstra_path
from networkx.algorithms.traversal import bfs_tree

from database.DAO import DAO


class Model:
    def __init__(self):
        self._g = nx.Graph()
        self._idAirports = dict()
        self.percorso = []
        self.numero_voli = 0

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
        nodes = self._g.neighbors(p)
        lista = list()
        for n in nodes:
            lista.append((n, self.numero_totale_voli(n)))
        lista.sort(key=lambda x: x[1], reverse=True)
        return lista



    def trovaPercorso(self, p, a, tratte):
        self.percorso = []
        self.numero_voli = 0
        raggiungibili = dfs_tree(self._g, a).nodes
        self.ricorsione([p], a, tratte, 0, raggiungibili)
        return self.percorso, self.numero_voli

    def ricorsione(self, parziale, arrivo, tratte, voli, raggiungibili):
        if parziale[-1] == arrivo:
            if self.numero_voli < voli:
                print(voli)
                self.percorso = copy.deepcopy(parziale)
                self.numero_voli = voli
                return
        elif tratte == 0:
            return
        else:
            u = parziale[-1]
            for v in self._g.neighbors(u):
                if v in raggiungibili:
                    parziale.append(v)
                    p = self._g[u][v]['weight']
                    self.ricorsione(parziale, arrivo, (tratte-1), (voli + p), raggiungibili)
                    parziale.pop()

    def numero_totale_voli(self, n):
        i = 0
        for v in self._g.neighbors(n):
            i += self._g[v][n]['weight']
        return i

    def sizeNodes(self):
        return len(self._g.nodes())

    def sizeEdges(self):
        return len(self._g.edges())