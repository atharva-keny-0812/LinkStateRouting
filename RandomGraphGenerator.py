'''
Project: Link State Routing Algorithm and Protocol
This code generates an Adjacency List which represents a graph comprising of Routers and Links
'''

import random

class RouterNetwork:
    def __init__(self):
        self.adjacency_list = {}
        self.n = 0

    # Function to generate a random weighted adjacency list for a graph representing routers and links
    def generate_graph(self, n, w):
        self.n = n
        # Initialize random number generator
        rng = random.Random()

        # Define the range of weights for link weights
        weight_range = (0, w)  # Change the range as needed

        # Initialize adjacency list
        self.adjacency_list = {i: [] for i in range(n)}  # Each node starts with an empty list of connections

        # Fill the adjacency list with random weights to represent links
        for i in range(n):
            for j in range(i + 1, n):
                # Assign a random weight to the edge (i, j) representing the link between routers
                weight = rng.randint(*weight_range)
                self.adjacency_list[i].append((j+1, weight))  # Add connection to i's list
                self.adjacency_list[j].append((i+1, weight))  # Add connection to j's list as it's bidirectional
        
        # Write the adjacency list to a file
        self._write_adjacency_list_to_file("AdjacencyList.txt")

    # Function to write adjacency list to a file
    def _write_adjacency_list_to_file(self, filename):
        with open(filename, 'w') as outFile:
            outFile.write(f"This is the global view of the Routers and the links attached to them along with their cost.\nEach entry in the list coresponds to router number and link cost respectively.\n\n")
            for node, connections in self.adjacency_list.items():
                outFile.write(f"Node {node+1}: {connections}\n")

    # Function to print adjacency list
    def _print_adjacency_list(self):
        for node, connections in self.adjacency_list.items():
            print(f"Router {node+1}: {connections}")

    # Function to print graph (public)
    def print_graph(self):
        print("Adjacency List representing router connectivity:")
        self._print_adjacency_list()
