# DeltaCodesONETEP

This repo provides all inputs to run DeltaCodesDFT using ONETEP.

## Input files
All input files used to calculate the Delta values are located in `work`
dir.

### Generate input files
```
python onetep_DELTA_test_gen.py ../DeltaCodesDFT/CIFs
! Copy pseudopotentials
bash get_pseudo.sh
```
Note that FM systems (Fe, Co and Ni) and AFM systems (O [↑↑↓↓], Cr [↑↓↑↓], and 
Mn[↑↓]) needs to be manually modified. And some calculations might not converge
with the generated inputs.

## Running calculations
```
ONETEP_PATH=/PATH/TO/ONETEP/EXE/onetep.ARCH
for element in $(ls -d */)
do

cd $element

cd 1.0
mpiexec $ONETEP_PATH | tee log
cd ../

for i in 0.94 0.96 0.98 1.02 1.04 1.06
do
cp 1.0/*.dkn 1.0/*.tightbox_ngwfs $i
cd $i
mpiexec $ONETEP_PATH | tee log
rm *.dkn *.tightbox_ngwfs
cd ../
done

cd ../

done
```

## Getting results
```
for element in $(ls -d */ | sed 's/\///g')
do

cd $element

name=$element
num_atoms=$(grep "Totals" 1.0/*95.onetep | awk '{print $2}')
edft=$(grep "edft" 1.0/*.dat | head -1 | awk '{print $3}')
bash ../../analyse/get_EOS.sh ../../analyse/get_EOS.py > EOS.dat
echo -n $element" ";
python ../../analyse/delta.py EOS.dat $edft $name $num_atoms | tail -3 | head -1 | awk '{print $2" "$3" "$4}'

cd ../

done
```
The Delta values can be obtained using
[DeltaCodesDFT](https://github.com/molmod/DeltaCodesDFT). The calculated
Equation of States can be found [here](./ONETEP.txt). The calculated Delta value
is 0.962 meV/Atom.
