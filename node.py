#
# Dijkstra's Algorithm, By Kieron Pang
# Node file
#

class Node:
    def __init__(self, name):
        self.name = name
        self.edge = []
        self.weight = []

    def getName(self):
        return self.name
    
    def getEdge(self):
        return self.edge
    
    def getWeight(self, pos):
        return self.weight[pos]
    
    def addNode(self, node):
        self.edge.append(node)

    def addWeight(self, weight):
        self.weight.append(weight)
    
    def addEdge(self, node, weight):
        self.addNode(node)
        self.addWeight(weight)

    def removeEdge(self, edge):
        self.edge.remove(edge)
    
    def removeWeight(self, weight):
        self.weight.remove(weight)

    def reset(self):
        self.edge = []
        self.weight = []