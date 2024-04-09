import RandomGraphGenerator as Router

def main():
    router_network = Router.RouterNetwork()

    # Get the number of routers from the user
    n = int(input("Enter the number of routers: "))
    w = int(input("Enter the max cost of going from one link to another: "))

    # Generate random weighted adjacency list representing router connectivity
    router_network.generate_graph(n,w)

    # Output the adjacency list
    router_network.print_graph()

if __name__ == "__main__":
    main()