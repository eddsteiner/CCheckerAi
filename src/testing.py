import numpy as np
import ctypes

import neat


print("hi")

a = np.array([-1, 2, 4, 0, 5, 3, 6, 2, 1], dtype = np.float32)
b = np.array([3, 0, 2, 3, 4, 5, 4, 7, 2], dtype = np.float32)
c = np.zeros(9, dtype = np.float32)

#apoint, read_only_flag = a.__array_interface__["data"]
#bpoint, read_only_flag = b.__array_interface__["data"]
#cpoint, read_only_flag = c.__array_interface__["data"]
apoint = a.ctypes.data
bpoint = b.ctypes.data
cpoint = c.ctypes.data

print("here")

neat.maxmul(apoint, bpoint, cpoint, 3)
print(c)


creature = neat.Creature()
x = creature.connection_count
print(x)
print(creature.total_gene_count())


generation_manager = neat.GenerationManager()
print(generation_manager.POPULATION_SIZE)




