import RandomGraphGenerator as RouterNetwork
import Router

def main():
    router_network = RouterNetwork.RouterNetwork()

    # Get the number of routers from the user
    n = int(input("Enter the number of routers: "))
    w = int(input("Enter the max cost of going from one link to another: "))

    # Generate random weighted adjacency list representing router connectivity
    router_network.generate_graph(n,w)

    # Output the adjacency list
    router_network.print_graph()

    router1=Router.Router()
    source = 1
    distances, predecessors = router1._dijkstra_(source, router_network.adjacency_list)
    routing_table = router1._create_routing_table(source, predecessors)
    print("Routing Table for Router 1:")
    print(routing_table)

if __name__ == "__main__":
    main()