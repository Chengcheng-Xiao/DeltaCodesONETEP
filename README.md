# DeltaCodesONETEP

This repo provides all inputs to run DeltaCodesDFT using ONETEP.

## Input files
All input files are located in `generate` dir.

### [Optional] Generate input files
```
python onetep_DELTA_test_gen.py ../DeltaCodesDFT/CIFs
! Copy pseudopotentials
bash get_pseudo.sh
```
Note that FM systems (Fe, Co and Ni) and AFM systems (O [↑↑↓↓], Cr [↑↓↑↓], and 
Mn[↑↓]) needs to manually modified.

## Running calculations [in element_dir]
```
cd element/1.0
mpirun -n ...
cd ../

for i in 0.94 0.96 0.98 1.02 1.04 1.06
do
cp 1.0/*.dkn 1.0/*.tightbox_ngwfs $i
cd $i
mpirun -n ...
rm *.dkn *.tightbox_ngwfs
cd ../
done
```

## Getting results [in element dir]
```
name=element
num_atoms=$(grep "Totals" 1.0/*95.onetep | awk '{print $2}')
edft=$(grep "edft" 1.0/*.dat|awk '{print $3}')
bash ../../analyse/get_EOS.sh ../../analylse/get_EOS.py > EOS.dat
python ../../analyse/delta.py EOS.dat $edft $name $num_atoms
```

### [Optional] To delete all dirs
```
rm -r $(ls -d */)
```
