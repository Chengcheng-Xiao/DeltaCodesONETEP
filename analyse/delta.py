import numpy as np
from ase.units import kJ
from ase.eos import EquationOfState as EOS
from ase.utils.deltacodesdft import delta
import sys
import os

# read-in data
filename = sys.argv[1]
# metal?
if sys.argv[2] == 'T':
    metal = True
else:
    metal = False
# check if file exist:
if os.path.exists(filename):
    pass
else:
    print(f"The file {filename} does not exist.")
    exit()
data = np.loadtxt(filename)
V = data[:,0]
if metal:
    E = data[:,2]
else:
    E = data[:,1]
num_atom= float(sys.argv[4])
element = sys.argv[3]

# volume in A^3/Atom, energy in eV/Atom
V=V/num_atom
E=E/num_atom

# EOS fitting
eos = EOS(V, E, 'birchmurnaghan')
eos.fit(warn=False)
e0, B, Bp, v0 = eos.eos_parameters
# eV, eV/A^3, unitless, A^3

from ase.collections import dcdft
dcdft_dct = dcdft.data[element]

v0_w2K = dcdft_dct['wien2k_volume']
B_w2K = dcdft_dct['wien2k_B']*1e-24*kJ # convert to eV/A^3
Bp_w2K = dcdft_dct['wien2k_Bp']

# v0, B, Bp, Delta_value
print('        V0(Å^3)      B0(Gpa)   B1')
print(f'ONETEP: {v0:0.10f} {B/(1e-24*kJ):0.10f} {Bp:0.10f}')
print(f'WIEN2K: {v0_w2K:0.10f} {B_w2K/(1e-24*kJ):0.10f} {Bp_w2K:0.10f}')

# note that delta code take B in eV/A^3
print(f'DELTA = {delta(v0, B, Bp, v0_w2K, B_w2K, Bp_w2K):0.10f}')
