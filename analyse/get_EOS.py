from ase.io import write,read
from ase.units import Hartree
import sys

Atoms=read('log', format='onetep-in')
Volume = Atoms.get_volume()

with open('log') as f:
    lines = f.readlines()
    Energy = [line for line in lines if 'Total energy' in line]
    Free_energy = [line for line in lines if 'Total free energy' in line]

    if len(Free_energy) > 0:
        Free_energy = float(Free_energy[-1].split()[3])*Hartree
    else:
        Free_energy = 0
    
    if len(Energy) > 0:
        Energy = float(Energy[-1].split()[3])*Hartree
    else:
        Energy = 0

print(f'{Volume} {Energy} {Free_energy}')

    
