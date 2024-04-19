import RandomGraphGenerator as RouterNetwork
import simpy
from Router import Router
import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(file, adjacency_list):
    # Create an empty graph
    graph = nx.Graph()

    # Add nodes to the graph
    graph.add_nodes_from(adjacency_list.keys())

    # Add edges to the graph based on the adjacency list
    for node, neighbors in adjacency_list.items():
        for neighbor, weight in neighbors:
            graph.add_edge(node, neighbor, weight=weight)

    # Draw the graph
    pos = nx.spring_layout(graph)  # Layout for better visualization
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_weight="bold")
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    # Save the plot as an ASCII-encoded PNG image
    plt.savefig(file, format='png', bbox_inches='tight', pad_inches=0.2)
    
    # Clear the plot to avoid overwriting
    plt.clf()

# Function to create n router objects and add them to a list
#Here network repersents entire connection of graph in form of adjacency list.
routers = [] #Contains n router objects
def create_routers(env,n, network):
    for i in range(1, n + 1):
        routers.append(Router(env, "Router" + str(i), network[i],i))
    # Establish connections after routers are created
    for i in range(n):
        for j in range(len(routers[i].neighbors)):
            if routers[i].neighbors[j][1] != 0:
                routers[i].connected_routers.extend([routers[routers[i].neighbors[j][0] - 1]])
    
def main():
    # Create a simulation environment
    env=simpy.Environment()
    router_network = RouterNetwork.RouterNetwork()
    
    # Get the number of routers from the user
    n = int(input("Enter the number of routers: "))
    w = int(input("Enter the max cost of going from one link to another: "))

    # Generate random weighted adjacency list representing router connectivity
    network = router_network.generate_graph(n,w)
   
    plot_graph('InitialGraph.png',network)

    # Print the path to the saved image on the terminal
    print("Router network created and saved as graph.png and AdjacencyList.txt in the current directory.")
    create_routers(env,n, network)

    env.run(until=100)

    plot_graph('NewGraph.png',routers[0].global_view)

    print("Updated routing tables after link failures for all routers:")
    for router in routers:
        print(f"Updated routing table for {router.name}: {router.routing_table}")
    
    print("-" * 100)
    print("We have successfully created the Routing Tables for our network of",n,"routers.\n")
    print("Now let us show a Demo of how a packet will be sent across this Routing Network\n")
    while True:
        source_node=int(input("Enter the source node: "))
        destination_node=int(input("Enter the destination node: "))
        print("-"*30)
        routers[source_node-1].sendpacket(source_node,destination_node,[])
        print("-"*30)
        repeat=input("Do you wish to see the demo again? (yes/no): ")
        if repeat=="no":
            break
        print()
        print("-"*30)

if __name__ == "__main__":
    main()