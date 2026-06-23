import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMapA = {}

    def getAllGenres(self):
        return DAO.getAllGenres()

    def buildGraph(self, genreId):

        nodi = DAO.getAllNodes(genreId)

        self._grafo.add_nodes_from(nodi)

        for node in nodi:
            self._idMapA[node.ArtistId] = node

        print(len(self._grafo.nodes))

        for u, v in DAO.getAllEdges(genreId, self._idMapA):
            if self._getPopolarita(u.ArtistId, genreId) > self._getPopolarita(v.ArtistId, genreId):
                self._grafo.add_edge(u, v,
                        weight=self._getPopolarita(u.ArtistId, genreId) + self._getPopolarita(v.ArtistId, genreId))
            elif self._getPopolarita(u.ArtistId, genreId) < self._getPopolarita(v.ArtistId, genreId):
                self._grafo.add_edge(v, u,
                        weight=self._getPopolarita(u.ArtistId, genreId) + self._getPopolarita(v.ArtistId, genreId))
            else:
                self._grafo.add_edge(u, v,
                        weight = self._getPopolarita(u.ArtistId, genreId) + self._getPopolarita(v.ArtistId, genreId))
                self._grafo.add_edge(v, u,
                        weight = self._getPopolarita(v.ArtistId, genreId) + self._getPopolarita(u.ArtistId, genreId))

        print(len(self._grafo.nodes))
        print(len(self._grafo.edges))

    def _getPopolarita(self, artistId, genreId):
        popolarita = DAO.getPopolaritaOfArtista(artistId, genreId)
        return popolarita[0]

    def getPath(self, v0):
        self._bestPath = []

        parziale = [v0]

        self._ricorsione(parziale)


    def _ricorsione(self, parziale):

        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        for n in self._grafo.neighbors(parziale[-1]):
            if n not in parziale:
                if len(parziale) > 1:
                    if self._grafo[parziale[-2]][parziale[-1]]["weight"] < self._grafo[parziale[-1]][n]["weight"]:
                        parziale.append(n)
                        self._ricorsione(parziale)
                        parziale.pop()
                else:
                    parziale.append(n)
                    self._ricorsione(parziale)
                    parziale.pop()
