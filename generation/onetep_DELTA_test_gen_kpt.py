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

def gen_input(element_in,kx,ky,kz,structure_path, mode):
    atoms = read(f'{structure_path}/{element_in}.cif')
    element = atoms[0].symbol

    # gen kpt list
    shift_x = 0; shift_y = 0; shift_z = 0
    # if even number, shift
    if kz%2==0:
        shift_z = 1/(2*kz)
    if ky%2==0:
        shift_y = 1/(2*ky)
    if kx%2==0:
        shift_x = 1/(2*kx)
    #  else:
    #      shift = 0

    # generate kpts
    kpts = monkhorst_pack([kx,ky,kz])
    # shift the grid to be gamma centered
    kpts[:,0] += shift_x
    kpts[:,1] += shift_y
    kpts[:,2] += shift_z
    num_kpts_unsym = kx*ky*kz
    
    kpt_weight = 1/num_kpts_unsym
    k_weight = np.full(num_kpts_unsym,kpt_weight)
    
    kpts_copy = kpts.copy()
    
    used = np.ones(num_kpts_unsym, dtype=bool)
    
    for nk in range(len(kpts)):
        print(nk)
        if not used[nk]:
            continue
        #  for nkr in range(nk+1,len(kpts_copy)):
        for nkr in range(len(kpts_copy)):
            if nk == nkr:
                continue
            #  ksd = kpts[nk] - kpts_copy[nkr]
            #  ksd = ksd - np.floor(ksd + 0.5)
            #  ksep= np.sum(ksd**2)
            #  if( exclude_minus_k ) then           ! Now test for related to -k if requested.
            if True:
                ksd=kpts[nk]+kpts_copy[nkr]
                ksd = ksd - np.floor(ksd + 0.5)
                ksep= np.sum(ksd**2)
                #  ksep = np.min((ksep,np.sum(ksd**2)))
            if (ksep < 1E-5**2):
                used[nkr] = False
                k_weight[nk] = k_weight[nk] + k_weight[nkr]
                k_weight[nkr] = 0.0
    
    kpt_list_fin = []
    kpt_weight_fin = []
    for nk in range(len(kpts)):
        #  print(nk)
        if used[nk]:
            kpt_list_fin.append(kpts[nk])
            kpt_weight_fin.append(k_weight[nk])

            #  print(kpts[nk,0],kpts[nk,1],kpts[nk,2],k_weight[nk])
    kpt_list_fin = np.array(kpt_list_fin)
    kpt_weight_fin = np.array(kpt_weight_fin)
    kpts = np.hstack((kpt_list_fin,kpt_weight_fin[:,np.newaxis]))

    #  # find gamma point
    #  # halve the grid and calculate weight
    #  gamma_idx=np.where(np.isclose(kpts[:,0],0) * np.isclose(kpts[:,1],0) *
    #                     np.isclose(kpts[:,2],0))[0][0]
    #  kpts = kpts[gamma_idx:]
    #  size_new = kpts.shape[0]
    #  # add weight
    #  weight = 2/((size_new-1)*2+1)
    #  weight_gamma = weight/2
    #  weight_array = np.full([kpts.shape[0],1],weight)
    #  weight_array[0,0] = weight_gamma
    #  kpts = np.hstack((kpts,weight_array))
    #  #first kpt cannot be gamma.
    #  kpts = np.append(kpts[1:],[kpts[0]],axis=0)

    # convert to string
    kpt_string = '\n'.join(' '.join('% 0.10f' %x for x in y) for y in kpts)

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
        'kpoints_list' : [kpt_string]
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
        'kpoints_list' : [kpt_string]
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
        'kpoints_list' : [kpt_string]
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
    #  elif mode == 'mag_metal_AFM':
    #      keywords =  keywords_mag_metal
    #  elif mode == 'mag_metal_FM':
    #      keywords =  keywords_mag_metal
    elif mode == 'metal':
        keywords = keywords_metal
        keywords_metal_cont = keywords_metal.copy()
        keywords_metal_cont['read_denskern'] = True
        keywords_metal_cont['read_tightbox_ngwfs'] = True
        keywords_count = keywords_metal_cont
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
    if ((i not in mag_metal_AFM) and (i not in mag_metal_FM)):
        print(element)
        if not os.path.exists(element):
            os.makedirs(element)
        for strain in [0.94,0.96,0.98,1.0,1.02,1.04,1.06]:
            if not os.path.exists(str(strain)):
                os.makedirs(str(strain))

    if i in non_metal:
        gen_input(element,kx,ky,kz, structure_path, 'non_metal')
        for strain in [0.94,0.96,0.98,1.0,1.02,1.04,1.06]:
            os.rename(f'{element}_{strain}.dat', f'{strain}/{element}.dat')
            shutil.move(f'{strain}',f'{element}')
    elif i in nobel_gas:
        gen_input(element,kx,ky,kz, structure_path, 'nobel_gas')
        for strain in [0.94,0.96,0.98,1.0,1.02,1.04,1.06]:
            os.rename(f'{element}_{strain}.dat', f'{strain}/{element}.dat')
            shutil.move(f'{strain}',f'{element}')
    elif i in mag_metal_AFM:
        #  gen_input(element,kx,ky,kz, structure_path, 'mag_metal')
        continue
    elif i in mag_metal_FM:
        #  gen_input(element,kx,ky,kz, structure_path, 'mag_metal')
        continue
    else:
        gen_input(element,kx,ky,kz, structure_path, 'metal')
        for strain in [0.94,0.96,0.98,1.0,1.02,1.04,1.06]:
            os.rename(f'{element}_{strain}.dat', f'{strain}/{element}.dat')
            shutil.move(f'{strain}',f'{element}')
