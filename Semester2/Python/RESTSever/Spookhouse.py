from Spook import *
import threading
import random

amount = 4
teamnames = ["alligator", "anteater", "armadillo", "auroch", "axolotl", "badger", "bat", "beaver", "buffalo", "camel", "chameleon", "cheetah", "chipmunk", "chinchilla", "chupacabra", "cormorant", "coyote", "crow", "dingo", "dinosaur", "dolphin", "duck", "elephant", "ferret", "fox", "frog", "giraffe", "gopher", "grizzly", "hedgehog", "hippo", "hyena", "jackal", "ibex", "ifrit", "iguana", "koala", "kraken", "lemur", "leopard", "liger", "llama", "manatee", "mink", "monkey", "narwhal", "nyan cat", "orangutan", "otter", "panda", "penguin", "platypus", "python", "pumpkin", "quagga", "rabbit", "raccoon", "rhino", "sheep", "shrew", "skunk", "slow loris", "squirrel", "turtle", "walrus", "wolf", "wolverine", "wombat"]
spooks = list()

class spook(threading.Thread):
    def __init__(self, teamname, speed):
        threading.Thread.__init__(self)
        self.teamname = teamname
        self.speed = speed
        self.Vehicle = None
    def run(self):
        self.Vehicle = generate_vehicle(self.teamname, self.speed)
        return self

for x in range(amount):
        spooks.append(spook(teamnames[x], random.uniform(0.1,0.3)))
for x in range(amount):
        spooks[x].start()

print('kleir')
