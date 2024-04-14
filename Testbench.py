import RandomGraphGenerator as RouterNetwork
import Router
import simpy

def broadcaster(env,routers):
    while True:
        for router in routers:
            yield env.timeout(2)
            router.broadcast(router.neighbours, router.number)
            break

# Function to create n router objects and add them to a list
def create_routers(env,n,adjacency_list):
    routers_list = []
    filtered_adjacency_list = {}

    for node, tuples_list in adjacency_list.items():
        filtered_tuples = [(a, b) for a, b in tuples_list if b != 0]
        if filtered_tuples:  # If there are any non-zero tuples
            filtered_adjacency_list[node] = filtered_tuples

    for i in range(n):
        name = "Router {}".format(i+1)
        ip_address = "192.168.0.{}".format(i+1)  # Example IP address generation
        router = Router.Router(env,name, i+1,ip_address,filtered_adjacency_list[i+1])
        routers_list.append(router)
    return routers_list

def main():
    # Create a simulation environment
    env=simpy.Environment()
    router_network = RouterNetwork.RouterNetwork()

    # Get the number of routers from the user
    n = int(input("Enter the number of routers: "))
    w = int(input("Enter the max cost of going from one link to another: "))

    # Generate random weighted adjacency list representing router connectivity
    router_network.generate_graph(n,w)

    # Output the adjacency list
    router_network.print_graph()

    # router1=Router.Router()
    # source = 1
    # distances, predecessors = router1._dijkstra_(source, router_network.adjacency_list)
    # routing_table = router1._create_routing_table(source, predecessors)
    # print("Routing Table for Router 1:")
    # print(routing_table)

    # routers_list = create_routers(env,n,router_network.adjacency_list)
    # for router in routers_list:
    #     for neighbour in router.connected_routers:
    #         router.neighbours[routers_list[neighbour[0]-1]]=neighbour[1]
    #         router.global_view[router.number]=router.neighbours
    
    # # Accessing routers in the list
    # for router in routers_list:
    #     print()
    #     print("Name:", router.name)
    #     print("Number:", router.number)
    #     print("IP Address:", router.ip_address)
    #     print("Connected Routers",router.connected_routers)
    #     print("Neighbours:")
    #     for neighbour in router.neighbours.keys():
    #         print(neighbour.name,end=" ")
    #     print()

    # # Run simulation
    # env.process(broadcaster(env,routers_list))
    # env.run(until=100)

    # # while env.peek() <= 1000:
    # #     if(env.peek()>t):
    # #         print("hello")
    # #     env.step()
    # #     t=int(env.now)

    # for router in routers_list:
    #     for i in router.global_view.keys():
    #         print(i,":")
    #         for j in router.global_view[i].keys():
    #             print(j.name,":",router.global_view[i][j])
    #             print()

if __name__ == "__main__":
    main()