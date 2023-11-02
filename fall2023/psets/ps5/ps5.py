from itertools import product, combinations

'''
Before you start: Read the README and the Graph implementation below.
'''

class Graph:
    '''
    A graph data structure with number of nodes N, list of sets of edges, and a list of color labels.

    Nodes and colors are both 0-indexed.
    For a given node u, its edges are located at self.edges[u] and its color is self.color[u].
    '''

    # Initializes the number of nodes, sets of edges for each node, and colors
    def __init__(self, N, edges = None, colors = None):
        self.N = N
        self.edges = [set(lst) for lst in edges] if edges is not None else [set() for _ in range(N)]
        self.colors = [c for c in colors] if colors is not None else [None for _ in range(N)]
    
    # Adds a node to the end of the list
    # Returns resulting graph
    def add_node(self):
        self.N += 1
        self.edges.append(set())
        return self
    
    # Adds an undirected edge from u to v
    # Returns resulting graph
    def add_edge(self, u, v):
        assert(v not in self.edges[u])
        assert(u not in self.edges[v])
        self.edges[u].add(v)
        self.edges[v].add(u)
        return self

    # Removes the undirected edge from u to v
    # Returns resulting graph
    def remove_edge(self, u, v):
        assert(v in self.edges[u])
        assert(u in self.edges[v])
        self.edges[u].remove(v)
        self.edges[v].remove(u)
        return self

    # Resets all colors to None
    # Returns resulting graph
    def reset_colors(self):
        self.colors = [None for _ in range(self.N)]
        return self

    def clone(self):
        return Graph(self.N, self.edges, self.colors)

    def clone_and_merge(self, g2, g1u, g2v):
        '''
        DOES NOT COPY COLORS
        '''
        g1 = self
        edges = g1.edges + [[v + g1.N for v in u_list] for u_list in g2.edges]
        g = Graph(g1.N + g2.N, edges)
        if g1u is not None and g2v is not None:
            g = g.add_edge(g1u, g2v + g1.N)
        return g

    # Checks all colors
    def is_graph_coloring_valid(self):
        for u in range(self.N):
            for v in self.edges[u]:

                # Check if every one has a coloring
                if self.colors[u] is None or self.colors[v] is None:
                    return False

                # Make sure colors on each edge are different
                if self.colors[u] == self.colors[v]:
                    return False
        
        return True

'''
    Introduction: We've implemented exhaustive search for you below.

    You don't need to implement any extra code for this part.
'''

# Given an instance of the Graph class G, exhaustively search for a k-coloring
# Returns the coloring list if one exists, None otherwise.
def exhaustive_search_coloring(G, k=3):

    # Iterate through every possible coloring of nodes
    for coloring in product(range(0,k), repeat=G.N):
        G.colors = list(coloring)
        if G.is_graph_coloring_valid():
            return G.colors

    # If no valid coloring found, reset colors and return None
    G.reset_colors()
    return None


'''
    Part A: Implement two coloring via breadth-first search.

    Hint: You will need to adapt the given BFS pseudocode so that it works on all graphs,
    regardless of whether they are connected.

    When you're finished, check your work by running python3 -m ps5_color_tests 2.
'''

## Student-Made Helper-Functions
def make_set(N):
    n_set = set()
    for i in range(N):
        n_set.add(i)
    return n_set

def print_graph(G):
    print("Adjacency List:")
    for i,v in enumerate(G.edges):
        print("Node",i,":",v)
    print()



# Given an instance of the Graph class G and a subset of precolored nodes,
# Assigns precolored nodes to have color 2, and attempts to color the rest using colors 0 and 1.
# Precondition: Assumes that the precolored_nodes form an independent set.
# If successful, modifies G.colors and returns the coloring.
# If no coloring is possible, resets all of G's colors to None and returns None.
def bfs_2_coloring(G, precolored_nodes=None):
    # Assign every precolored node to have color 2
    # Initialize visited set to contain precolored nodes if they exist
    visited = set()
    frontier = set()
    G.reset_colors()
    preset_color = 2
    if precolored_nodes is not None:
        for node in precolored_nodes:
            G.colors[node] = preset_color
            visited.add(node)

        if len(precolored_nodes) == G.N:
            print("Entire set already pre-colored")
            print("Colors:",G.colors)
            return G.colors
    
    # TODO: Complete this function by implementing two-coloring using the colors 0 and 1.
    # If there is no valid coloring, reset all the colors to None using G.reset_colors()
    # print()
    # print("PRINTING FOR BFS 2-COLORING ...")
    # print()
    # print_graph(G)
    unvisited = make_set(G.N)
    #Go through all vertices
    while len(visited) < G.N:
        #find next node (also accounts for if next node is on a new island)
        frontier = {list(unvisited)[0]}
        
        if G.colors[list(unvisited)[0]] != 2:
            G.colors[list(unvisited)[0]] = 0

        unvisited.remove(list(unvisited)[0])
        temp_set = set()
        # print("Start of Island:",frontier)
        while frontier:
            # print("Before checking neighbors: T:",G.N,"| F:",frontier,"| V:",visited, "| U:",unvisited)
            #do bfs
            for node_index in frontier:
                visited.add(node_index)
                for neighbor in G.edges[node_index]:
                    if neighbor in unvisited:
                        # Frontier nodes colored here
                        current_color = G.colors[node_index]
                        next_color = 1 if current_color == 0 else 0
                        # print("NOTE, current color is",current_color,"next-color is ",next_color)
                        # print("Since node",node_index,"is color",current_color, end=" ")
                        # print("We have to color node",neighbor, "in color", next_color)
                        if G.colors[neighbor] != 2:
                            G.colors[neighbor] = next_color
                        else:
                            # print(neighbor,"is PRECOLORED")
                            pass
                                
                        
                        temp_set.add(neighbor)
                        unvisited.remove(neighbor)
            frontier = temp_set.copy()
            temp_set.clear()
            visited = visited.union(frontier)

            # print("Finished checking neighbors:","T:",G.N,"| F:",frontier,"| V:",visited, "| U:",unvisited,"\n")
    # print("Final Colors: ",G.colors)

    if G.is_graph_coloring_valid():
        # print("Coloring is valid!✅")
        return G.colors
    else:
        # print("Coloring is NOT valid!❌")
        G.reset_colors()

    return None

'''
    Part B: Implement is_independent_set.
'''

# Given an instance of the Graph class G and a subset of precolored nodes,
# Checks if subset is an independent set in G 
def is_independent_set(G, subset):
    # TODO: Complete this function
    
    visited = set()
    for node_index in subset:
        for neighbor in G.edges[node_index]:
            if neighbor in visited:
                #print("We've already visited this element. Not an ind. set!")
                return False
            visited.add(neighbor)

    return True

'''
    Part C: Implement the 3-coloring algorithm from the sender receiver exercise.
    
    Make sure to call the bfs_2_coloring and is_independent_set functions that you already implemented!

    Hint 1: You will want to use the Python `combinations` function from the itertools library
    to enumerate all possible independent sets. Remember that each element of combinations is a tuple,
    so you may need to convert it to a list.

    Hint 2: Python itertools functions compute their results lazily, which means that they only
    calculate each element as the program requests it. This saves time and space, since it
    doesn't need to store the entire list of combinations up front. You should NOT try to convert the result
    of the entire combinations call to a list, since that will force Python to precompute everything.
    Instead, you should iterate over them in a for loop, which will maintain the lazy behavior we want.
    See the call to "product" in exhaustive_search for an example.

    When you're finished, check your work by running python3 -m ps5_color_tests 3.
    Don't worry if some of your tests time out: that is expected.
'''

# Given an instance of the Graph class G (which has a subset of precolored nodes), searches for a 3 coloring
# If successful, modifies G.colors and returns the coloring.
# If no coloring is possible, resets all of G's colors to None and returns None.
def iset_bfs_3_coloring(G):
    # TODO: Complete this function.
    iteration = 0
    # if G.N < 30:
    #     return None
    for i in range(0,(G.N//3)+1):
        for ind_set in combinations(range(0,G.N), r=i):
            # print("iteration=",iteration)
            if is_independent_set(G,ind_set):
                # print("N =",G.N, "|", iteration, "is an ind_set, so let's check if it's 2-colorable...",end="")
                if bfs_2_coloring(G,ind_set) != None:
                    # print("✅",iteration,"is two-colorable!")
                    return G.colors
                else:
                    # print(iteration,"is not two-colorable ❌")
                    pass
            iteration+=1
    print("NO 2-Colorable IND SET FOUND! ❌❌")
    G.reset_colors()
    return None

# Feel free to add miscellaneous tests below!
if __name__ == "__main__":
    G0 = Graph(3).add_edge(0, 1).add_edge(1, 2)
    G1 = Graph(4).add_edge(0,1).add_edge(1,2).add_edge(2,3)
    G2 = Graph(6).add_edge(0,3).add_edge(1,4).add_edge(2,5)
    GInd = Graph(3)
    bfs_2_coloring(G1,{0,1,2,3})
    # print(bfs_2_coloring(G0))
    # iset_bfs_3_coloring(G1)
    # print(is_independent_set(G=G2,subset=GInd))
    # print("Adjacency List:")
    # for i,v in enumerate(G1.edges):
    #     print("Node",i,":",v)
    # print()
    # print("Exhaustive Coloring:")
    # exhaustive_search_coloring(G1)
    # for i,v in enumerate(G1.colors):
    #     print("Node",i,":","COLOR",v)
    # print()
    # print("BFS 2-Coloring:")
    # bfs_2_coloring(G1)
    # for i,v in enumerate(G1.colors):
    #     print("Node",i,":","COLOR",v)
