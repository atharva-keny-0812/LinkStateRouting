import simpy
import random
import heapq

class Router:
    def __init__(self, env, name, neighbors,number):
        self.env = env
        self.name = name
        self.neighbors = neighbors
        self.connected_routers=[]
        self.messages_received = []
        self.number=number
        self.global_view={number:neighbors}
        self.action = env.process(self.run(env))
        self.routing_table={}

    def run(self,env):
        while True:
            random_number = random.randint(1, 100)
            if env.peek() > 60 and random_number <-1:
                self.fail_link()
            
            # Considering Maximum of 15 routers and a delay of 2s to transfer information from one router to another in a skewed network.
            

            if env.peek()%30==0 and env.peek()!=0:
                self._complete_global_view()
                _, predecessors = self._dijkstra_(self.number, self.global_view)
                self._create_routing_table(self.number, predecessors)
                # Print routing tables for all routers
            if env.peek() % 20 ==  0 and env.peek() != 0:
                print("Routing tables created for all routers:")
                print(f"Current simulation time: {env.now}, Routing table for {self.name}: {self.routing_table}")
                print("________________________________________________________________________________________________")
            
            if (env.peek()-1)%30==0 and env.peek()!=1:
                self.messages_received=[]

            message = yield self.env.process(self.receive())
            self.forward(None,message)

    def receive(self):
        # Simulate receiving a message
        yield self.env.timeout(1)
        return ((f"Message from {self.name}"),self.neighbors,self.number)

    def forward(self, sender, message):
        # Forward the message to all neighbors except the one it received from
        name=self.name
        for neighbor in self.connected_routers:
            if neighbor.name!=sender:
                if message[0] in neighbor.messages_received:
                    continue
                neighbor.messages_received.append(message[0])
                neighbor.global_view[message[2]]=message[1]
                neighbor.forward(name,message)

    def fail_link(self):
        # Select a random neighbor to fail
        if self.neighbors:
            neighbor_to_fail = random.choice(self.neighbors)
            neighbor_index = neighbor_to_fail[0]
            if neighbor_index == self.number:
                return
            # Set the weight of the selected neighbor to 0 to simulate link failure
            print(f"{self.name}: Link failure detected with Router {neighbor_index}")
            for tup in self.neighbors:
                if tup == neighbor_to_fail:
                    self.neighbors.remove(tup)
                    break
            for router in self.connected_routers:
                if router.number == neighbor_index:
                    neighbor_to_fail_obj = router
                    neighbor_to_fail_obj.received_fail_link(self)
                    self.connected_routers.remove(router)
            self.global_view[neighbor_index]=self.neighbors
            self._complete_global_view()
            

    def received_fail_link(self, neighbour):    
        for tup in self.neighbors:
            if tup[0] == neighbour.number:
                self.neighbors.remove(tup)
                break
        for router in self.connected_routers:
                if router.number == neighbour.number:
                    self.connected_routers.remove(router)
        self.global_view[neighbour.number]=self.neighbors
        self._complete_global_view()

    def sendpacket(self,source_node,destination_node):
        if self.number==destination_node:
            print(self.name,": I have received message from Router",destination_node)
            return
        nexthop=self.routing_table[destination_node]
        print(self.name,"I am forwarding Router",destination_node,"'s message to Router",nexthop)
        for router in self.connected_routers:
            if router.number==nexthop:
                router.sendpacket(source_node,destination_node)
                break

    def _dijkstra_(self, source, adjacency_list):
        # Initialize distances and predecessors dictionaries
        distances = {node: float('inf') for node in adjacency_list}
        predecessors = {node: None for node in adjacency_list}
        distances[source] = 0

        # Initialize priority queue
        pq = [(0, source)]

        while pq:
            # Extract the node with the minimum distance from the priority queue
            current_distance, current_node = heapq.heappop(pq)

            # Iterate over neighbors of the current node
            for neighbor, weight in adjacency_list[current_node]:
                if weight == 0:  # Skip links with zero weight
                    continue

                distance = current_distance + weight

                # If the distance through the current node is shorter than the previously recorded distance to the neighbor
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node  # Update predecessor
                    heapq.heappush(pq, (distance, neighbor))

        return distances, predecessors
    
    def _get_shortest_path_(self, source, target, predecessors):
        path = []
        node = target
        while node is not None:
            path.insert(0, node)
            node = predecessors[node]
        return path
    
    def _create_routing_table(self, source, predecessors):
        for node in predecessors:
            if node != source:
                shortest_path = self._get_shortest_path_(source, node, predecessors)
                if len(shortest_path) >= 2:
                    next_hop = shortest_path[1]  # Next hop is the second node in the shortest path
                else:
                    next_hop = -1
                self.routing_table[node] = next_hop

    def _complete_global_view(self):
        num_routers=len(list(self.global_view.keys()))
        for neighbours in self.global_view.items():
            visited=[-1]*(num_routers+1)
            for neighbour in neighbours[1]:
                visited[neighbour[0]]=1
            for i in range(1,num_routers+1):
                if(visited[i]==-1):
                    self.global_view[neighbours[0]].append((i,0))
