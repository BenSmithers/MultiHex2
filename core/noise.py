import numpy as np

def perlin(self):
    nodes = 100

    xs = np.random.rand(2*nodes,nodes)
    ys = np.sqrt(1.0-xs**2)

    