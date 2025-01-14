from ase.io import read
import numpy as np
import sys

filename = sys.argv[1] # path to file
atoms=read(filename)
rec_lat = atoms.cell.reciprocal().array*np.pi*2
rec_vol = np.linalg.det(rec_lat)

rec_len = np.linalg.norm(rec_lat, axis=-1)
print(np.ceil(rec_len/0.0754))


