#470 Group project 1
# Morgan Aylene Jack

# prims algorithm
#purpose: maze with no loops and exactly one path between any two points
import sys

class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]

        
        #utility function to print the constructed MST stored in parent[]
        def printMST(self, parent):
            print("Edge \tWeight") 
            for i in range(1,self.V):
                print(parent[i],"-",i,"\t", self.graph[parent[i]][i])

        #find the vertex with minimum distance value form the set of vertices 
        #not yet included in the shortest path tree
        def minKey(self,key,mstSet):
            min = sys.maxsize
            for v in range(self.V):
                if key[v] < min and mstSet[v] == False:
                    min =key[v]
                    min_index = v
            return min_index
        
        #construct and print MST for a graph represented using adj matrix representation
        def primMST(self):
            #key values used to picl minimum weight edge in cut
            key = [sys.maxsize] * self.V
            parent = [None]* self.V

            #first vertex
            key[0]=0
            mstSet = [False] * self.V
            parent[0] = -1 #root node

            for cout in range(self.V):

                # u is always equal to the source in first iteration
                u = self.minKey(key,mstSet)

                # min distance vertex in the shortest path tree
                mstSet[u] = True

                # for loop for val of the vertex dependant on the distance
                for v in range (self.V):
                    if self.graph[u][v] > 0 and mstSet[v] == False \
                                and key[v] > self.graph[u]:
                        [v]: key[v] = self.graph[u]
                        [v]
                        parent[v] =u
                        self.printMST(parent)
    
    
    
    if __name__ == '__main__':
        g = Graph(5)
    g.graph = [[0, 2, 0, 6, 0],
                [2, 0, 3, 8, 5],
                [0, 3, 0, 0, 7],
                [6, 8, 0, 0, 9],
                [0, 5, 7, 9, 0]]

    g.primMST()



