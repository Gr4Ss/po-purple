from Spook.py import all
import threading
import random

amount = 5
teamnames = ["alligator", "anteater", "armadillo", "auroch", "axolotl", "badger", "bat", "beaver", "buffalo", "camel", "chameleon", "cheetah", "chipmunk", "chinchilla", "chupacabra", "cormorant", "coyote", "crow", "dingo", "dinosaur", "dolphin", "duck", "elephant", "ferret", "fox", "frog", "giraffe", "gopher", "grizzly", "hedgehog", "hippo", "hyena", "jackal", "ibex", "ifrit", "iguana", "koala", "kraken", "lemur", "leopard", "liger", "llama", "manatee", "mink", "monkey", "narwhal", "nyan cat", "orangutan", "otter", "panda", "penguin", "platypus", "python", "pumpkin", "quagga", "rabbit", "raccoon", "rhino", "sheep", "shrew", "skunk", "slow loris", "squirrel", "turtle", "walrus", "wolf", "wolverine", "wombat"]

for x in range(amount):
	spook = threading.Thread(target= generate_vehicle(teamnames[randint(0,len(teamnames)-1)], random.uniform(0.1,0.3))
	spook.setDeamon(True)
	spook.start()
