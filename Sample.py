import simpy
import random
import heapq

class Router:
    def __init__(self, env, name, neighbors,number,adjacency_list):
        self.env = env
        self.name = name
        self.neighbors = neighbors
        self.connected_routers=[]
        self.messages_received = []
        self.number=number
        # self.ip_address = ip_address
        self.global_view={number:neighbors}

        self.action = env.process(self.run(env))
        self.routing_table={}
        self.haha=adjacency_list

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
                # print(neighbour[0])
                visited[neighbour[0]]=1
            for i in range(1,num_routers+1):
                if(visited[i]==-1):
                    self.global_view[neighbours[0]].append((i,0))
        

    def run(self,env):
        while True:

            if env.peek() % 60 ==  0 and env.peek() != 0:
                self.fail_link()
            
            # Considering Maximum of 15 routers and a delay of 2s to transfer information from one router to another in a skewed network.
            if env.peek()%30==0 and env.peek()!=0:
                # print(self.name,": ",self.messages_received,self.global_view)
                self._complete_global_view()
                print(self.name,"mera global view",self.global_view)
                # print(env.peek(),":Lo Chala mai Dijkstra ko call karne ~",self.name)
                _, predecessors = self._dijkstra_(self.number, self.global_view)
                # print("Kiska hai ye tumko intazar Dijkstra aagaya na ~",self.name)
                self._create_routing_table(self.number, predecessors)
                # print("Dekhlo idhar to  Routing Table Taiyar ho gaya na ~",self.name)

            if (env.peek()-1)%30==0 and env.peek()!=1:
                print(env.peek(),":Flooding starts again for",self.name)
                self.messages_received=[]

            # if env.peek()%40==0 and env.peek()!=0:
            #     # print(env.peek(),":Lo Chala mai Dijkstra ko call karne ~",self.name)
            #     _, predecessors = self._dijkstra_(self.number, self.global_view)
            #     # print("Kiska hai ye tumko intazar Dijkstra aagaya na ~",self.name)
            #     self._create_routing_table(self.number, predecessors)
            #     # print("Dekhlo idhar to  Routing Table Taiyar ho gaya na ~",self.name)
            	
            message = yield self.env.process(self.receive())
            # print("I am Transmittinng my info ~ ",self.name)
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
                # print("I am forwarding Router",message[2]," info to",neighbor.name,"~",self.name)
                if message[0] in neighbor.messages_received:
                    continue
                neighbor.messages_received.append(message[0])
                neighbor.global_view[message[2]]=message[1]
                # print("Now ",neighbor.name," will forward")
                neighbor.forward(name,message)

    def fail_link(self):
        # Select a random neighbor to fail
        if self.neighbors:
            neighbor_to_fail = random.choice(self.neighbors)
            neighbor_index = neighbor_to_fail[0]
            if neighbor_index == self.number:
                return
            # Set the weight of the selected neighbor to 0 to simulate link failure
            # print(self.name, "my neighbours:", self.neighbors)
            print(self.name,": Mai tujhse Rishta Nata Todta huun Router",neighbor_to_fail[0])
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
