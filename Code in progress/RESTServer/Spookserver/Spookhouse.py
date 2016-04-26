from Spook import *
import threading
import random, requests,time
amount = 5
teamnames = ["alligator", "anteater", "armadillo", "auroch", "axolotl", "badger", "bat", "beaver", "buffalo", "camel", "chameleon", "cheetah", "chipmunk", "chinchilla", "chupacabra", "cormorant", "coyote", "crow", "dingo", "dinosaur", "dolphin", "duck", "elephant", "ferret", "fox", "frog", "giraffe", "gopher", "grizzly", "hedgehog", "hippo", "hyena", "jackal", "ibex", "ifrit", "iguana", "koala", "kraken", "lemur", "leopard", "liger", "llama", "manatee", "mink", "monkey", "narwhal", "nyan cat", "orangutan", "otter", "panda", "penguin", "platypus", "python", "pumpkin", "quagga", "rabbit", "raccoon", "rhino", "sheep", "shrew", "skunk", "slow loris", "squirrel", "turtle", "walrus", "wolf", "wolverine", "wombat"]
spooks = list()

class spook(threading.Thread):
    def __init__(self, teamname, speed):
        threading.Thread.__init__(self)
        self.daemon = True
        self.teamname = teamname
        self.speed = speed
        self.Vehicle = None
    def run(self):
        self.Vehicle = generate_vehicle(self.teamname, self.speed)
        return self

def add_parcels():
    count = 1
    while True:
        requests.put("http://localhost:9000/parcels/add", json=json.dumps({"secretkey":"SecretKey","newParcels":[[count,random.randint(1,4),random.randint(1,4)]]}))
        count += 1
        time.sleep(5)
t = threading.Thread(target = add_parcels)
t.setDaemon(True)
t.start()
for x in range(amount):
        ind = random.randint(0,len(teamnames)-1)
        spooks.append(spook(teamnames.pop(ind), random.uniform(0.1,0.3)))
for x in range(amount):
        spooks[x].start()
while True:
    pass
print('kleir')
