class Graph():

    def __init__(self, graph_dict):
        '''
        Simple data structure to represent the graph as a dictionary
        Ex.
        {
        'A' : ['B'],
        'B' : ['A']
        }
        A <-> B
        '''
        self.graph = graph_dict
    
    def add_edges(self, vertice, edges):
        self.graph[vertice].extend(edges)

    def add_vertice(self, vertice, edges):
        self.graph[vertice] = edges

    def edges(self, vertice):
        return self.graph[vertice]

    def vertices(self):
        return list(self.graph.keys())

if __name__ == '__main__':
    print(help(Graph))