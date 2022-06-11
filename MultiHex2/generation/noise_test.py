import matplotlib
matplotlib.use('GTK3Agg')
from matplotlib import pyplot as plt
import numpy as np

from MultiHex2.generation.utils import perlin

i_scale = 256
seed = 5
print("seed: {}".format(seed))
other = 5
noise = perlin(i_scale,other, seed)
noise += perlin(i_scale, other*2,seed)
noise += perlin(i_scale, 2,seed)

plt.pcolormesh(noise, cmap='coolwarm')
plt.colorbar()
plt.show()
plt.clf()
