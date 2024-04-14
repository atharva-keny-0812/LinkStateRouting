import RandomGraphGenerator as RouterNetwork
# import Router
import simpy
from Sample import Router

# def broadcaster(env,routers):
#     while True:
#         for router in routers:
#             yield env.timeout(2)
#             router.broadcast(router.neighbours, router.number)
#             break

# Function to create n router objects and add them to a list
#Here network repersents entire connection of graph in form of adjacency list.
routers = [] #Contains n router objects
def create_routers(env,n, network):
    print(network)
    for i in range(1, n + 1):
        # neigh = []
        # for j in range(n):
        #     neigh.append((list(network.values())[j]))
        routers.append(Router(env, "Router" + str(i), network[i],i))
        neigh = []
    print(routers[1].neighbors)
    # Establish connections after routers are created
    for i in range(n):
        for j in range(len(routers[i].neighbors)):
            print(i, j)
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

    # Output the adjacency list
    router_network.print_graph()
    create_routers(env,n, network)

    env.run(until=10)
    # # Print messages received by each router
    # print("Messages received by Router A:", router_a.messages_received,router_a.global_view)
    # print("Messages received by Router B:", router_b.messages_received,router_b.global_view)
    # print("Messages received by Router C:", router_c.messages_received,router_c.global_view)
    for i in range(n):
        print("Messages received by Router:" + str(i + 1), routers[i].messages_received,routers[i].global_view)

if __name__ == "__main__":
    main()
