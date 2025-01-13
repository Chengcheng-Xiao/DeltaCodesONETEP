import numpy as np

from ase.build import graphene_nanoribbon
from ase.calculators.onetep import Onetep
from ase.io import write,read
from ase.dft.kpoints import monkhorst_pack
from numpy.linalg import norm
import sys
import shutil
import os
import pandas as pd

structure_path = sys.argv[1]

def gen_input(element_in,kx,ky,kz,structure_path,magmom,magmom_string,mode):
    atoms = read(f'{structure_path}/{element_in}.cif')
    element = atoms[0].symbol

    # gen kpt list
    shift_x = 0; shift_y = 0; shift_z = 0
    # if even number, shift
    if kz%2==0:
        shift_z = 1
    if ky%2==0:
        shift_y = 1
    if kx%2==0:
        shift_x = 1

    # convert to string
    kpt_string = f'{kx} {ky} {kz}' 
    kpt_shift_string = f'{shift_x} {shift_y} {shift_z}'

    keywords_non_metal = {
        'output_detail': 'Normal',
        'task' : 'SinglePoint',

        'cutoff_energy' : '1280 eV',
        'xc_functional' : 'PBE',

        'use_cmplx_ngwfs' : True,
        'extend_ngwf' : 'T T T',
        'kpoint_method' : 'KP',
        'full_rand_ngwf' : True,
        'rand_seed_ngwf_dynamic' : False,
        'permit_unusual_ngwf_count' : True,
        'maxit_ngwf_cg' : 1000,
        'write_forces' : 'F',
        'spin' : 0,
        'spin_polarized' : False,

        'do_properties': False,
        'species_pot' : [f'{element} {element}_NCP19_PBE_OTF.usp'],
        'kpoint_grid_size' : kpt_string,
        'kpoint_grid_shift' : kpt_shift_string
    }

    keywords_nobel_gas= {
        'output_detail': 'Normal',
        'task' : 'SinglePoint',

        'cutoff_energy' : '1280 eV',
        'xc_functional' : 'PBE',

        'use_cmplx_ngwfs' : True,
        'extend_ngwf' : 'T T T',
        'kpoint_method' : 'KP',
        'full_rand_ngwf' : True,
        'rand_seed_ngwf_dynamic' : False,
        'permit_unusual_ngwf_count' : True,
        'maxit_ngwf_cg' : 1000,
        'write_forces' : 'F',
        'maxit_lnv' : -1,
        'minit_lnv' : -1,
        'spin' : 0,
        'spin_polarized' : False,


        'do_properties': False,
        'species_pot' : [f'{element} {element}_NCP19_PBE_OTF.usp'],
        'kpoint_grid_size' : kpt_string,
        'kpoint_grid_shift' : kpt_shift_string
    }

    keywords_metal = {
        'output_detail': 'Normal',
        'task' : 'SinglePoint',

        'cutoff_energy' : '1280 eV',
        'xc_functional' : 'PBE',

        'edft': True,
        'edft_maxit': 4,
        'edft_smearing_width' : '0.2 eV',
        'eigensolver_orfac': '-1',
        'eigensolver_abstol': '-1',
        'occ_mix' : 1.0,
        'spin' : 0,
        'spin_polarized' : False,

        'use_cmplx_ngwfs' : True,
        'extend_ngwf' : 'T T T',
        'kpoint_method' : 'KP',
        'full_rand_ngwf' : True,
        'rand_seed_ngwf_dynamic' : False,
        'permit_unusual_ngwf_count' : True,
        'maxit_ngwf_cg' : 1000,
        'write_forces' : 'F',

        'do_properties': False,
        'species_pot' : [f'{element} {element}_NCP19_PBE_OTF.usp'],
        'kpoint_grid_size' : kpt_string,
        'kpoint_grid_shift' : kpt_shift_string
    }

    keywords_metal_mag = {
        'output_detail': 'Normal',
        'task' : 'SinglePoint',

        'cutoff_energy' : '1280 eV',
        'xc_functional' : 'PBE',

        'edft': True,
        'edft_maxit': 4,
        'edft_smearing_width' : '0.2 eV',
        'eigensolver_orfac': '-1',
        'eigensolver_abstol': '-1',
        'occ_mix' : 1.0,

        'spin' : magmom,
        'spin_polarized' : True,
        'ngwfs_spin_polarized' : True,
        'edft_spin_fix' : 5,

        'use_cmplx_ngwfs' : True,
        'extend_ngwf' : 'T T T',
        'kpoint_method' : 'KP',
        'full_rand_ngwf' : True,
        'rand_seed_ngwf_dynamic' : False,
        'permit_unusual_ngwf_count' : True,
        'maxit_ngwf_cg' : 1000,
        'write_forces' : 'F',

        'do_properties': False,
        'species_pot' : [f'{element} {element}_NCP19_PBE_OTF.usp'],
        'kpoint_grid_size' : kpt_string,
        'kpoint_grid_shift' : kpt_shift_string
    }

    if mode == 'non_metal':
        keywords = keywords_non_metal
        keywords_non_metal_cont = keywords_non_metal.copy()
        keywords_non_metal_cont['read_denskern'] = True
        keywords_non_metal_cont['read_tightbox_ngwfs'] = True
        keywords_count = keywords_non_metal_cont

    elif mode == 'nobel_gas':
        keywords =  keywords_nobel_gas
        keywords_nobel_gas_cont = keywords_nobel_gas.copy()
        keywords_nobel_gas_cont['read_denskern'] = True
        keywords_nobel_gas_cont['read_tightbox_ngwfs'] = True
        keywords_count = keywords_nobel_gas_cont
    elif mode == 'metal':
        keywords = keywords_metal
        keywords_metal_cont = keywords_metal.copy()
        keywords_metal_cont['read_denskern'] = True
        keywords_metal_cont['read_tightbox_ngwfs'] = True
        keywords_count = keywords_metal_cont
    elif mode == 'mag_metal':
        keywords =  keywords_metal_mag
        keywords_metal_mag_cont = keywords_metal_mag.copy()
        keywords_metal_mag_cont['read_denskern'] = True
        keywords_metal_mag_cont['read_tightbox_ngwfs'] = True
        keywords_count = keywords_metal_mag_cont
    else:
        print('no corresponding config.')
        exit()

    # create 7 files by applying strain
    frac_pos = atoms.get_scaled_positions()
    cell = atoms.cell

    # create 1.0 input
    atoms_tmp = atoms.copy()
    atoms_tmp.set_cell(cell)
    atoms_tmp.set_scaled_positions(frac_pos)
    if magmom_string!='NONE':
        atoms_tmp.set_initial_magnetic_moments(magmom_string)
    write(f'{element}_1.0.dat', atoms_tmp, format='onetep-in',
          keywords=keywords)

    # create strained 0.94 - 1.06 input
    for strain in [0.94,0.96,0.98,1.02,1.04,1.06]:
        atoms_tmp = atoms.copy()
        atoms_tmp.set_cell(cell*(strain**(1/3)))
        atoms_tmp.set_scaled_positions(frac_pos)
        write(f'{element}_{strain}.dat', atoms_tmp, format='onetep-in', keywords
              =keywords_count)
    return

#------------------------------------------------------------------------------
non_metal = [1,6,7,9,15,16,17,34,35,53,85]
nobel_gas = [2,10,18,36,54,86]
mag_metal_AFM = [8,24,25]
mag_metal_FM = [26,27,28]

df = pd.read_csv('CASTEP.csv',index_col=0)


# i => atomic idx
for i in df.index.values.tolist():
    element = df['Element'][i]
    kx = df['kx'][i]
    ky = df['ky'][i]
    kz = df['kz'][i]

    # make dirs
    print(element)
    if not os.path.exists(element):
        os.makedirs(element)
    for strain in [0.94,0.96,0.98,1.0,1.02,1.04,1.06]:
        if not os.path.exists(str(strain)):
            os.makedirs(str(strain))

    if i in non_metal:
        mag_string = 'NONE'
        gen_input(element,kx,ky,kz, structure_path,0.0,mag_string,'non_metal')
        for strain in [0.94,0.96,0.98,1.0,1.02,1.04,1.06]:
            os.rename(f'{element}_{strain}.dat', f'{strain}/{element}.dat')
            shutil.move(f'{strain}',f'{element}')
    elif i in nobel_gas:
        mag_string = 'NONE'
        gen_input(element,kx,ky,kz, structure_path,0.0,mag_string,'nobel_gas')
        for strain in [0.94,0.96,0.98,1.0,1.02,1.04,1.06]:
            os.rename(f'{element}_{strain}.dat', f'{strain}/{element}.dat')
            shutil.move(f'{strain}',f'{element}')
    elif i in mag_metal_AFM:
        if i == 8:
            mag_string = [1,1,-1,-1]
        if i == 24:
            mag_string = [1,-1,1,-1]
        if i == 25:
            mag_string = [1,-1]
        mag_string = 'NONE'
        gen_input(element,kx,ky,kz, structure_path,0.0,mag_string,'mag_metal')
        for strain in [0.94,0.96,0.98,1.0,1.02,1.04,1.06]:
            os.rename(f'{element}_{strain}.dat', f'{strain}/{element}.dat')
            shutil.move(f'{strain}',f'{element}')
    elif i in mag_metal_FM:
        mag_string = 'NONE'
        gen_input(element,kx,ky,kz, structure_path,1.0,mag_string,'mag_metal')
        for strain in [0.94,0.96,0.98,1.0,1.02,1.04,1.06]:
            os.rename(f'{element}_{strain}.dat', f'{strain}/{element}.dat')
            shutil.move(f'{strain}',f'{element}')
    else:
        mag_string = 'NONE'
        gen_input(element,kx,ky,kz, structure_path,0.0,mag_string,'metal')
        for strain in [0.94,0.96,0.98,1.0,1.02,1.04,1.06]:
            os.rename(f'{element}_{strain}.dat', f'{strain}/{element}.dat')
            shutil.move(f'{strain}',f'{element}')

#  8 O conf=2s2.0 2p4.0 INIT SPIN= CHARGE=0
#  24 Cr conf=3s2.0 3p6.0 3d5.0 4s1.0 4p0.0 INIT SPIN= CHARGE=0
#  25 Mn conf=3s2.0 3p6.0 3d5.0 4s2.0 4p0.0 INIT SPIN= CHARGE=0
#
#  26 Fe conf=3s2 3p6 3d5 4s0 4p0 INIT SPIN= CHARGE=0
#  27 Co conf=3s2.0 3p6.0 3d7.0 4s2.0 4p0.0 INIT SPIN= CHARGE=0
#  28 Ni conf=3s2.0 3p6.0 3d8.0 4s2.0 4p0.0 INIT SPIN= CHARGE=0
#
