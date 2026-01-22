# DeltaCodesONETEP

This repo provides all inputs to run DeltaCodesDFT using ONETEP.

## Input files
### Generate input files [optional]
```
python onetep_DELTA_test_gen.py ../DeltaCodesDFT/CIFs
! Copy pseudopotentials
bash get_pseudo.sh
```
Note that FM systems (Fe, Co and Ni) and AFM systems (O [↑↑↓↓], Cr [↑↓↑↓], and
Mn[↑↓]) needs to be manually modified. And some calculations might have trouble
converge with the generated inputs.

### Tested Input files
All tested input files that has been tested and used to calculate the Delta
values can be found in in `work` directory.

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

cd 1.0
rm *.dkn *.tightbox_ngwfs
cd ../

cd ../

done
```

## Getting the equation of states and Delta values
```
for element in $(ls -d */ | sed 's/\///g')
do

cd $element

name=$element
num_atoms=$(grep "Totals" 1.0/*.onetep | awk '{print $2}')
edft=$(grep "edft" 1.0/*.dat | head -1 | awk '{print $3}')
bash ../../analyse/get_EOS.sh ../../analyse/get_EOS.py > EOS.dat
echo -n $element" ";
python ../../analyse/delta.py EOS.dat $edft $name $num_atoms | tail -3 | head -1 | awk '{print $2" "$3" "$4}'

cd ../

done
```

This will generate the `EOS.dat` file for each element, which contains the
equilibrium volume, bulk modulus and the pressure derivative of the bulk
modulus.

The calculated Equation of States for all elements can be found in
[ONETEP_EOS.txt](./ONETEP_EOS.txt). 

The Delta values can be obtained using
[DeltaCodesDFT](https://github.com/molmod/DeltaCodesDFT). E.g.,


```
python calcDelta.py ONETEP.txt WIEN2k.txt --stdout
```

The calculated average Delta value is 0.989 meV/Atom.

-------------------------------------------------------------------------------

## GENERAL INFORMATION

- exchange-correlation functional: PBE
- relativistic scheme: scalar relativistic (Koelling-Harmon)
- assignment of core / valence states: see
  [table](README.md#table-of-parameters)
- basis set size grid density: see [table](README.md#table-of-parameters)
- k-mesh density: see [table](README.md#table-of-parameters) (grid values and
  number of k-points in the irreducible wedge of the 1st Brillouin zone (#k));
this choice achieves spacing ∆k < 0.0754 A−1; Grid is Gamma-centered.
- reciprocal-space integration method: Fermi-Dirac smearing with a fictitious
  temperature corresponding to 0.05 eV
- Density kernel treatment:
  - Li-Nunes-Vanderbilt (LNV): H, N, F, P, Cl
  - Fixed kernel: He, Ne, Ar, Kr, Xe, Rn
  - ensemble dft (EDFT): rest of the elements

## METHOD-SPECIFIC INFORMATION
- pseudopotential library: CASTEP “on-the-fly” optimized norm-conserving
  Vanderbilt (ONCVPSP). Settings for “NCP19” library release 
  
- pseudopotential core radii: see [table](README.md#table-of-parameters) (rc) 
- local channel: see [table](README.md#table-of-parameters) (lloc) 
- non-local core radii: Same as rc. 
- number of projectors: Mostly 1 per valence l channel plus 1 per semi-core
  state, except for O (2s and 2p) , Cr-Ni (3d), Nb (4d), W and Re (5p), Lu, Ir,
  Pt, Au (5p and 5d) and Pb (6s, 6p, 5d) where 2 per channel were used.
- projector generation: KE-Optimized RRKJ. 
- pseudization radius for NLCC core charge 0.7 rc 

## Table of parameters

Calculation settings and results per element: valence, pseudopotential core
radius rc, local channel lloc, projector wave vector cutoﬀ qc, Monkhorst-Pack
k-point mesh in the full 1st Brillouin zone of the conventional cell kpts and
number of irreducible k-points #k, real-space grid mesh, equilibrium volume per
atom V0, bulk modulus B0, pressure derivative of the bulk modulus B1.

|      |Element|Valence      |rc  |lloc|qc  |k_a|k_b|k_c|#k  |g_a|g_b|g_c|V0(A^3/atom)  |B0[GPa]       |B1[-]        |
|------|-------|-------------|----|----|----|---|---|---|----|---|---|---|--------------|--------------|-------------|
|1     |H      |1s1          |0.8 |1   |8   |25 |25 |17 |585 |21 |21 |25 |17.3288926145 |10.3473251608 |2.6245067879 |
|2     |He     |1s2          |1   |1   |8   |33 |33 |18 |1080|21 |21 |27 |17.2747841842 |1.0094775173  |6.5492706927 |
|3     |Li     |1s22s1       |1.2 |1   |8   |32 |32 |32 |3009|39 |39 |39 |20.1782744985 |13.7970002366 |4.3936720483 |
|4     |Be     |1s22s2       |1.1 |1   |9   |43 |43 |24 |2288|13 |13 |21 |7.9124121649  |124.4055371235|3.3244742414 |
|5     |B      |2s22p1       |1.2 |1   |8   |21 |21 |20 |2321|25 |25 |25 |7.2237682364  |235.6593542125|3.4417643296 |
|6     |C      |2s22p2       |1.2 |1   |8   |39 |39 |10 |882 |13 |13 |45 |11.6547965851 |206.6772599314|3.5552671180 |
|7     |N      |2s22p3       |1.1 |1   |9   |14 |14 |14 |176 |35 |35 |35 |29.0092710418 |52.4096191085 |3.5976957960 |
|8     |O      |2s22p4       |1.2 |2   |9   |22 |20 |20 |2442|25 |25 |25 |18.3824268937 |51.0489198161 |3.8370658663 |
|9     |F      |2s22p5       |1.4 |2   |8   |14 |23 |13 |1104|33 |21 |33 |19.1015253981 |34.0574249332 |3.9328633245 |
|10    |Ne     |2s22p6       |1.4 |2   |8   |19 |19 |19 |220 |25 |25 |25 |23.5931437284 |1.6098247315  |7.0402444055 |
|11    |Na     |2s22p63s1    |1.5 |2   |8   |26 |26 |26 |1652|45 |45 |45 |37.2762293759 |6.5821046865  |24.825947746 |
|12    |Mg     |3s2          |1.8 |1   |-   |31 |31 |17 |864 |15 |15 |25 |22.7566608916 |36.4416385099 |4.0287290337 |
|13    |Al     |3s23p1       |1.6 |1   |-   |21 |21 |21 |286 |21 |21 |21 |16.4554708479 |77.2324174994 |4.3896771799 |
|14    |Si     |3s23p2       |1.6 |1   |-   |27 |27 |27 |560 |21 |21 |21 |20.4127635204 |88.3448980601 |4.3004165871 |
|15    |P      |3s23p3       |1.59|1   |-   |26 |8  |19 |700 |21 |55 |25 |21.4099093302 |68.2186821782 |4.4160547028 |
|16    |S      |3s23p4       |1.8 |1   |-   |33 |33 |33 |3281|13 |13 |13 |17.0840243267 |84.2294526459 |4.1813420174 |
|17    |Cl     |3s23p5       |1.59|1   |6   |11 |20 |10 |396 |39 |21 |45 |38.5655108638 |19.1339708445 |4.2782282959 |
|18    |Ar     |3s23p6       |1.6 |2   |6   |15 |15 |15 |120 |33 |33 |33 |51.5240015483 |0.7976299119  |7.8245470473 |
|19    |K      |3s23p64s1    |1.5 |2   |6   |16 |16 |16 |165 |25 |25 |25 |73.3791351110 |3.6164588206  |4.3325534958 |
|20    |Ca     |3s23p64s2    |2   |3   |6   |16 |16 |16 |165 |27 |27 |27 |42.2250471715 |17.4592529374 |3.3520793316 |
|21    |Sc     |3s23p63d14s2 |1.8 |3   |7   |29 |29 |17 |765 |21 |21 |25 |24.6267964151 |54.6439767534 |3.3471200672 |
|22    |Ti     |3s23p63d24s2 |1.79|3   |7   |33 |33 |18 |1080|15 |15 |25 |17.4494623722 |112.6537466734|3.5599567000 |
|23    |V      |3s23p63d34s2 |1.6 |3   |7   |28 |28 |28 |680 |21 |21 |21 |13.4432724586 |183.2500405865|3.7987805063 |
|24    |Cr     |3s23p63d54s1 |1.3 |3   |10.5|30 |30 |30 |816 |21 |21 |21 |11.8842699141 |160.5357726127|4.2466354497 |
|25    |Mn     |3s23p63d54s2 |1.3 |3   |10.5|24 |24 |24 |1183|21 |21 |21 |11.6479753476 |154.2714781410|1.9787655661 |
|26    |Fe     |3s23p63d64s2 |1.29|3   |10.5|30 |30 |30 |816 |21 |21 |21 |11.3439248908 |183.6415920685|7.6939078725 |
|27    |Co     |3s23p63d74s2 |1.3 |3   |10.5|39 |39 |21 |1617|15 |15 |25 |10.7912877276 |226.6580784609|3.7375486574 |
|28    |Ni     |3s23p63d84s2 |1.3 |3   |10.5|24 |24 |24 |455 |25 |25 |25 |10.8476456924 |199.7905726766|4.9497979540 |
|29    |Cu     |3d104s1      |1.81|3   |4.5 |23 |23 |23 |364 |21 |21 |21 |11.9979817571 |139.1280212584|4.9264004541 |
|30    |Zn     |3d104s2      |1.81|3   |4.5 |37 |37 |17 |1197|15 |15 |33 |15.1651699799 |77.9905326352 |4.6056540512 |
|31    |Ga     |3d104s24p1   |1.81|3   |4.5 |19 |11 |19 |600 |27 |45 |27 |20.3488624599 |48.7705369338 |5.2713796221 |
|32    |Ge     |3d104s24p2   |1.79|3   |5   |26 |26 |26 |511 |25 |25 |25 |23.9606788050 |59.0505352761 |4.7397728168 |
|33    |As     |3d104s24p3   |1.8 |3   |5.5 |26 |26 |8  |518 |25 |25 |63 |22.7274383850 |69.8690581661 |3.8641766039 |
|34    |Se     |3d104s24p4   |1.8 |3   |6   |22 |22 |17 |788 |27 |27 |33 |30.0710387351 |47.5941812541 |3.8207992716 |
|35    |Br     |3d104s24p5   |1.8 |3   |6   |11 |20 |10 |396 |49 |25 |55 |39.9006444216 |22.7219752577 |4.8595217527 |
|36    |Kr     |4s24p6       |1.9 |2   |-   |13 |13 |13 |84  |33 |33 |33 |65.2978327469 |0.6945519932  |8.1650200700 |
|37    |Rb     |4s24p65s1    |2.09|2   |-   |15 |15 |15 |120 |33 |33 |33 |91.0419691852 |2.8309766455  |4.4823864513 |
|38    |Sr     |4s24p65s2    |2   |3   |-   |14 |14 |14 |120 |33 |33 |33 |54.5233708331 |11.7207793437 |3.1933641766 |
|39    |Y      |4s24p64d15s2 |2   |3   |-   |27 |27 |15 |600 |21 |21 |33 |32.7209804258 |41.8453799370 |3.2288308258 |
|40    |Zr     |4s24p64d25s2 |2.1 |3   |-   |30 |30 |17 |819 |21 |21 |33 |23.4416936608 |96.3561183127 |3.3054846383 |
|41    |Nb     |4s24p64d45s1 |1.4 |3   |8   |26 |26 |26 |560 |21 |21 |21 |18.1627539753 |169.0384109307|3.7366103999 |
|42    |Mo     |4s24p64d55s1 |1.4 |2   |8   |27 |27 |27 |560 |21 |21 |21 |15.8346409170 |259.2650718645|4.2321106936 |
|43    |Tc     |4s24p64d65s1 |1.4 |2   |8   |35 |35 |19 |1200|15 |15 |25 |14.4607247062 |299.9910882754|4.5309864559 |
|44    |Ru     |4s24p64d75s1 |1.39|2   |8   |36 |36 |20 |1397|13 |13 |21 |13.7684926419 |314.7053513487|4.8440838491 |
|45    |Rh     |4s24p64d85s1 |1.4 |2   |8   |22 |22 |22 |364 |21 |21 |21 |14.0323688126 |259.6690101269|5.1905974736 |
|46    |Pd     |4s24p64d105s0|1.5 |2   |8   |22 |22 |22 |364 |25 |25 |25 |15.3258618012 |169.0507149820|5.6218539965 |
|47    |Ag     |4s24p64d105s1|1.5 |2   |8   |21 |21 |21 |286 |25 |25 |25 |17.8351330677 |90.9424723008 |5.8205841865 |
|48    |Cd     |4s24p64d105s2|1.5 |2   |9   |32 |32 |15 |816 |21 |21 |33 |22.5766444094 |47.1679459562 |6.8191354158 |
|49    |In     |4d105s25p1   |2.61|3   |6   |26 |26 |17 |945 |21 |21 |33 |27.6605243229 |34.9221088333 |5.2452738227 |
|50    |Sn     |4d105s25p2   |2.6 |3   |6   |22 |22 |22 |328 |27 |27 |27 |36.9848106593 |35.5290434442 |4.8861341384 |
|51    |Sb     |5s25p3       |2.59|2   |6   |22 |22 |8  |380 |25 |25 |65 |31.8413935494 |50.7944185718 |4.5611691355 |
|52    |Te     |5s25p4       |2.2 |2   |-   |22 |22 |14 |656 |25 |25 |33 |35.0103806406 |44.9855139548 |4.7425260799 |
|53    |I      |5s25p5       |2.2 |2   |-   |10 |19 |9  |300 |49 |25 |63 |50.5428182963 |18.6000298565 |5.0607892190 |
|54    |Xe     |5s25p6       |2.19|2   |-   |12 |12 |12 |84  |39 |39 |39 |86.2433878996 |0.5611821561  |8.0821658995 |
|55    |Cs     |5s25p66s1    |2.19|2   |5   |14 |14 |14 |120 |35 |35 |35 |116.6599984899|1.9989007905  |3.2108018562 |
|56    |Ba     |5s25p66s2    |2   |2   |5.5 |17 |17 |17 |165 |33 |33 |33 |63.0453519544 |8.8354859301  |2.3020409928 |
|71    |Lu     |5s25p65d16s2 |1.8 |2   |8   |28 |28 |16 |720 |21 |21 |33 |29.2485314737 |46.8664401815 |3.3277515909 |
|72    |Hf     |5s25p65d26s2 |1.8 |2   |8   |31 |31 |17 |864 |21 |21 |33 |22.5556633080 |104.3553257112|3.3390123132 |
|73    |Ta     |5s25p65d36s2 |1.79|2   |8   |26 |26 |26 |560 |21 |21 |21 |18.2597944055 |187.7498565029|3.6115113042 |
|74    |W      |5s25p65d46s2 |1.6 |3   |8   |27 |27 |27 |560 |21 |21 |21 |16.1357457829 |303.1533165789|4.2087803594 |
|75    |Re     |5s25p65d56s2 |1.81|3   |8   |35 |35 |19 |1200|15 |15 |25 |14.9572990198 |363.8090967578|4.4459131368 |
|76    |Os     |5s25p65d66s2 |1.8 |2   |8   |35 |35 |20 |1320|15 |15 |25 |14.2937727572 |390.1241408015|4.7803039275 |
|77    |Ir     |5s25p65d76s2 |1.6 |3   |7   |22 |22 |22 |364 |21 |21 |21 |14.4940670671 |347.3989094863|5.1133523622 |
|78    |Pt     |5s25p65d96s1 |1.6 |3   |7   |21 |21 |21 |286 |25 |25 |25 |15.6207275254 |248.9381378820|5.4651600458 |
|79    |Au     |5s25p65d106s1|1.6 |3   |7   |20 |20 |20 |286 |25 |25 |25 |17.9511405545 |139.5424454365|5.9637651427 |
|80    |Hg     |5d106s2      |2.79|3   |5   |21 |21 |24 |858 |25 |25 |21 |29.5552488003 |6.9740390878  |3.8587081385 |
|81    |Tl     |5d106s26p1   |2.8 |3   |5   |27 |27 |15 |600 |21 |21 |33 |31.4741213373 |26.7796441132 |5.4774201161 |
|82    |Pb     |5d106s26p2   |2.4 |3   |7   |17 |17 |17 |165 |33 |33 |33 |31.9369521999 |39.9090248495 |4.2553625779 |
|83    |Bi     |6s26p3       |2.2 |2   |7   |21 |21 |7  |303 |25 |25 |75 |36.7170609659 |43.2915303381 |4.5464407046 |
|84    |Po     |6s26p4       |2.19|2   |7   |25 |25 |25 |455 |21 |21 |21 |37.5495965378 |45.7765506609 |4.9453258944 |
|86    |Rn     |6s26p6       |2.2 |2   |7   |12 |12 |12 |84  |45 |45 |45 |93.0921243586 |0.5234233260  |14.712477813 |
