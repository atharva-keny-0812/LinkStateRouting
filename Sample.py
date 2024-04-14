import simpy

class Router:
    def __init__(self, env, name, neighbors,number):
        self.env = env
        self.name = name
        self.neighbors = neighbors
        self.connected_routers=[]
        self.messages_received = []
        self.number=number
        # self.ip_address = ip_address
        self.global_view={number:neighbors}

        self.action = env.process(self.run())

    def run(self):
        while True:
            message = yield self.env.process(self.receive())
            self.forward(None,message)

    def receive(self):
        # Simulate receiving a message
        yield self.env.timeout(5)
        return ((f"Message from {self.name}"),self.neighbors,self.number)

    def forward(self, sender, message):
        # Forward the message to all neighbors except the one it received from
        name=self.name
        if message[0] in self.messages_received:
            return
        for neighbor in self.connected_routers:
            if neighbor.name!=sender:
                neighbor.messages_received.append(message[0])
                neighbor.global_view[message[2]]=message[1]
                neighbor.forward(name,message)


env = simpy.Environment()

# Create routers
router_a = Router(env, "Router A", [(2, 0), (3, 3)],1)
router_b = Router(env, "Router B", [(1, 0), (3, 4)],2)
router_c = Router(env, "Router C", [(1, 3), (2, 4)],3)

# Establish connections after routers are created
router_a.connected_routers.extend([router_c])
router_b.connected_routers.extend([router_c])
router_c.connected_routers.extend([router_a, router_b])

# Run the simulation
env.run(until=10)

# Print messages received by each router
print("Messages received by Router A:", router_a.messages_received,router_a.global_view)
print("Messages received by Router B:", router_b.messages_received,router_b.global_view)
print("Messages received by Router C:", router_c.messages_received,router_c.global_view)
