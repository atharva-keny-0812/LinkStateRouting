import simpy
import random
import heapq

class Router:
    
    def __init__(self,env, name, number,ip_address,connected_routers):
        self.env=env
        self.name = name
        self.number=number
        self.ip_address = ip_address
        self.connected_routers=connected_routers
        self.neighbours={}
        self.global_view={}

    def broadcast(self,neighbours,number):
        print("I am called by ",self.name)
        for neighbour in self.neighbours.keys():
            # Broadcast information to neighbors
            self.env.process(self.send_packet(neighbour,neighbours,number))

    def send_packet(self, receiver, packet, packet_number):
        # Send packet to receiver
        print("I am sending Packet to:",receiver.name)
        receiver.receive_packet(packet,packet_number)

    def receive_packet(self, neighbours, number):
        # Store received packet
        if number not in self.global_view.keys():
            print("I am ",self.name,"and have received information of Router",number)
            self.global_view[number]=neighbours
            print("I am ",self.name,"calling Broadcast for Router",number)
            self.broadcast(neighbours,number)



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
        routing_table = {}
        for node in predecessors:
            if node != source:
                shortest_path = self._get_shortest_path_(source, node, predecessors)
                next_hop = shortest_path[1]  # Next hop is the second node in the shortest path
                routing_table[node] = next_hop
        return routing_table

