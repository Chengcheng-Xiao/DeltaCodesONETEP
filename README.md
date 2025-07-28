# DeltaCodesONETEP

This repo provides all inputs to run DeltaCodesDFT using ONETEP.

## Input files
### Generate input files
```
python onetep_DELTA_test_gen.py ../DeltaCodesDFT/CIFs
! Copy pseudopotentials
bash get_pseudo.sh
```
Note that FM systems (Fe, Co and Ni) and AFM systems (O [↑↑↓↓], Cr [↑↓↑↓], and
Mn[↑↓]) needs to be manually modified. And some calculations might have trouble
converge with the generated inputs.

### Tested Input files
All input files that has been tested and used to calculate the Delta values can
be found in in `work` directory.

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
|1     |H      |1s1          |0.8 |1   |8   |25 |25 |17 |585 |21 |21 |25 |17.3288919667 |10.3473264835 |2.6245869796 |
|2     |He     |1s2          |1   |1   |8   |33 |33 |18 |1080|21 |21 |27 |17.2747842461 |1.0095057690  |6.5502741111 |
|3     |Li     |1s22s1       |1.2 |1   |8   |32 |32 |32 |3009|39 |39 |39 |20.1987670368 |14.1873846144 |2.9752133760 |
|4     |Be     |1s22s2       |1.1 |1   |9   |43 |43 |24 |2288|13 |13 |21 |7.9124120462  |124.4055465395|3.3245055219 |
|5     |B      |2s22p1       |1.2 |1   |8   |21 |21 |20 |2321|25 |25 |25 |7.2237681598  |235.6593664885|3.4417870780 |
|6     |C      |2s22p2       |1.2 |1   |8   |39 |39 |10 |882 |13 |13 |45 |11.6547965778 |206.6772363597|3.5552640487 |
|7     |N      |2s22p3       |1.1 |1   |9   |14 |14 |14 |176 |35 |35 |35 |29.0092699097 |52.4097417208 |3.5978255158 |
|8     |O      |2s22p4       |1.2 |2   |9   |22 |20 |20 |2442|25 |25 |25 |18.3824265149 |51.0488131153 |3.8370138875 |
|9     |F      |2s22p5       |1.4 |2   |8   |14 |23 |13 |1104|33 |21 |33 |19.1015299580 |34.0568533528 |3.9320031300 |
|10    |Ne     |2s22p6       |1.4 |2   |8   |19 |19 |19 |220 |25 |25 |25 |23.5942832316 |1.6203408681  |7.1982513948 |
|11    |Na     |2s22p63s1    |1.5 |2   |8   |26 |26 |26 |1652|45 |45 |45 |37.2817475693 |6.5816320527  |24.4403863044|
|12    |Mg     |3s2          |1.8 |1   |-   |31 |31 |17 |864 |15 |15 |25 |22.7566609027 |36.4416419525 |4.0287287733 |
|13    |Al     |3s23p1       |1.6 |1   |-   |21 |21 |21 |286 |21 |21 |21 |16.4554708636 |77.2324171469 |4.3896753134 |
|14    |Si     |3s23p2       |1.6 |1   |-   |27 |27 |27 |560 |21 |21 |21 |20.4127636386 |88.3448646071 |4.3003863161 |
|15    |P      |3s23p3       |1.59|1   |-   |26 |8  |19 |700 |21 |55 |25 |21.4099101843 |68.2187012740 |4.4159678174 |
|16    |S      |3s23p4       |1.8 |1   |-   |33 |33 |33 |3281|13 |13 |13 |17.0840241761 |84.2294595778 |4.1813611090 |
|17    |Cl     |3s23p5       |1.59|1   |6   |11 |20 |10 |396 |39 |21 |45 |38.5655066742 |19.1338713181 |4.2784283724 |
|18    |Ar     |3s23p6       |1.6 |2   |6   |15 |15 |15 |120 |33 |33 |33 |51.5255754329 |0.7959468584  |7.7276736846 |
|19    |K      |3s23p64s1    |1.5 |2   |6   |16 |16 |16 |165 |25 |25 |25 |73.3787486294 |3.6168504806  |4.3462786483 |
|20    |Ca     |3s23p64s2    |2   |3   |6   |16 |16 |16 |165 |27 |27 |27 |42.2250013951 |17.4618544165 |3.3348239303 |
|21    |Sc     |3s23p63d14s2 |1.8 |3   |7   |29 |29 |17 |765 |21 |21 |25 |24.6275508526 |54.6458553652 |3.2740010274 |
|22    |Ti     |3s23p63d24s2 |1.79|3   |7   |33 |33 |18 |1080|15 |15 |25 |17.4494606805 |112.6536090761|3.5601676275 |
|23    |V      |3s23p63d34s2 |1.6 |3   |7   |28 |28 |28 |680 |21 |21 |21 |13.4432742217 |183.2498785679|3.7984967677 |
|24    |Cr     |3s23p63d54s1 |1.3 |3   |10.5|30 |30 |30 |816 |21 |21 |21 |11.8845982822 |160.5935206451|4.1853161650 |
|25    |Mn     |3s23p63d54s2 |1.3 |3   |10.5|24 |24 |24 |1183|21 |21 |21 |11.6440136805 |148.7376649349|3.9644649539 |
|26    |Fe     |3s23p63d64s2 |1.29|3   |10.5|30 |30 |30 |816 |21 |21 |21 |11.3439230683 |183.6409922053|7.6942791077 |
|27    |Co     |3s23p63d74s2 |1.3 |3   |10.5|39 |39 |21 |1617|15 |15 |25 |10.7912874044 |226.6580712368|3.7375403815 |
|28    |Ni     |3s23p63d84s2 |1.3 |3   |10.5|24 |24 |24 |455 |25 |25 |25 |10.8476396138 |199.7922607934|4.9510546683 |
|29    |Cu     |3d104s1      |1.81|3   |4.5 |23 |23 |23 |364 |21 |21 |21 |11.9979819343 |139.1279253786|4.9263955169 |
|30    |Zn     |3d104s2      |1.81|3   |4.5 |37 |37 |17 |1197|15 |15 |33 |15.1651606163 |77.9914739846 |4.6067583866 |
|31    |Ga     |3d104s24p1   |1.81|3   |4.5 |19 |11 |19 |600 |27 |45 |27 |20.3489179128 |48.7707733598 |5.2653060332 |
|32    |Ge     |3d104s24p2   |1.79|3   |5   |26 |26 |26 |511 |25 |25 |25 |23.9606493291 |59.0499214551 |4.7424853116 |
|33    |As     |3d104s24p3   |1.8 |3   |5.5 |26 |26 |8  |518 |25 |25 |63 |22.7274563854 |69.8692873291 |3.8624992063 |
|34    |Se     |3d104s24p4   |1.8 |3   |6   |22 |22 |17 |788 |27 |27 |33 |30.0769465701 |47.6397398009 |3.4957185995 |
|35    |Br     |3d104s24p5   |1.8 |3   |6   |11 |20 |10 |396 |49 |25 |55 |39.9029608856 |23.2875200589 |4.2514965816 |
|36    |Kr     |4s24p6       |1.9 |2   |-   |13 |13 |13 |84  |33 |33 |33 |65.2822747688 |0.6920474114  |8.4735219312 |
|37    |Rb     |4s24p65s1    |2.09|2   |-   |15 |15 |15 |120 |33 |33 |33 |91.0379292644 |2.8189281945  |4.5734613344 |
|38    |Sr     |4s24p65s2    |2   |3   |-   |14 |14 |14 |120 |33 |33 |33 |54.5234008100 |11.7208007336 |3.1921843824 |
|39    |Y      |4s24p64d15s2 |2   |3   |-   |27 |27 |15 |600 |21 |21 |33 |32.7209789823 |41.8453677052 |3.2289193485 |
|40    |Zr     |4s24p64d25s2 |2.1 |3   |-   |30 |30 |17 |819 |21 |21 |33 |23.4416948503 |96.3560914545 |3.3053409025 |
|41    |Nb     |4s24p64d45s1 |1.4 |3   |8   |26 |26 |26 |560 |21 |21 |21 |18.1627540984 |169.0383925259|3.7365949434 |
|42    |Mo     |4s24p64d55s1 |1.4 |2   |8   |27 |27 |27 |560 |21 |21 |21 |15.8346401979 |259.2652203106|4.2321771851 |
|43    |Tc     |4s24p64d65s1 |1.4 |2   |8   |35 |35 |19 |1200|15 |15 |25 |14.4607251365 |299.9910067152|4.5309227087 |
|44    |Ru     |4s24p64d75s1 |1.39|2   |8   |36 |36 |20 |1397|13 |13 |21 |13.7684919141 |314.7055231082|4.8441983111 |
|45    |Rh     |4s24p64d85s1 |1.4 |2   |8   |22 |22 |22 |364 |21 |21 |21 |14.0323685976 |259.6691148218|5.1906357377 |
|46    |Pd     |4s24p64d105s0|1.5 |2   |8   |22 |22 |22 |364 |25 |25 |25 |15.3258595337 |169.0509655466|5.6221751661 |
|47    |Ag     |4s24p64d105s1|1.5 |2   |8   |21 |21 |21 |286 |25 |25 |25 |17.8351186162 |90.9442144630 |5.8224618693 |
|48    |Cd     |4s24p64d105s2|1.5 |2   |9   |32 |32 |15 |816 |21 |21 |33 |22.5766899014 |47.1611666713 |6.8125377986 |
|49    |In     |4d105s25p1   |2.61|3   |6   |26 |26 |17 |945 |21 |21 |33 |27.6605174698 |34.9220304186 |5.2458119283 |
|50    |Sn     |4d105s25p2   |2.6 |3   |6   |22 |22 |22 |328 |27 |27 |27 |36.9848086200 |35.5291556178 |4.8862149805 |
|51    |Sb     |5s25p3       |2.59|2   |6   |22 |22 |8  |380 |25 |25 |65 |31.8413931484 |50.7943852744 |4.5612176068 |
|52    |Te     |5s25p4       |2.2 |2   |-   |22 |22 |14 |656 |25 |25 |33 |35.0103767636 |44.9854994103 |4.7427722132 |
|53    |I      |5s25p5       |2.2 |2   |-   |10 |19 |9  |300 |49 |25 |63 |50.5427643766 |18.5987839775 |5.0645075358 |
|54    |Xe     |5s25p6       |2.19|2   |-   |12 |12 |12 |84  |39 |39 |39 |86.2361479369 |0.5630560684  |8.2748596497 |
|55    |Cs     |5s25p66s1    |2.19|2   |5   |14 |14 |14 |120 |35 |35 |35 |116.6588281404|1.9990087493  |3.2323414279 |
|56    |Ba     |5s25p66s2    |2   |2   |5.5 |17 |17 |17 |165 |33 |33 |33 |63.0454694875 |8.8355382328  |2.2975944542 |
|71    |Lu     |5s25p65d16s2 |1.8 |2   |8   |28 |28 |16 |720 |21 |21 |33 |29.2485427875 |46.8661563627 |3.3267604502 |
|72    |Hf     |5s25p65d26s2 |1.8 |2   |8   |31 |31 |17 |864 |21 |21 |33 |22.5556421127 |104.4251748934|3.3119511941 |
|73    |Ta     |5s25p65d36s2 |1.79|2   |8   |26 |26 |26 |560 |21 |21 |21 |18.2597956223 |187.7497897359|3.6113796364 |
|74    |W      |5s25p65d46s2 |1.6 |3   |8   |27 |27 |27 |560 |21 |21 |21 |16.1357422769 |303.1538841020|4.2092492630 |
|75    |Re     |5s25p65d56s2 |1.81|3   |8   |35 |35 |19 |1200|15 |15 |25 |14.9572999687 |363.8092316826|4.4457758262 |
|76    |Os     |5s25p65d66s2 |1.8 |2   |8   |35 |35 |20 |1320|15 |15 |25 |14.2937729800 |390.1241524316|4.7802705516 |
|77    |Ir     |5s25p65d76s2 |1.6 |3   |7   |22 |22 |22 |364 |21 |21 |21 |14.4940678986 |347.3992342007|5.1131813910 |
|78    |Pt     |5s25p65d96s1 |1.6 |3   |7   |21 |21 |21 |286 |25 |25 |25 |15.6207269696 |248.9383803126|5.4652673216 |
|79    |Au     |5s25p65d106s1|1.6 |3   |7   |20 |20 |20 |286 |25 |25 |25 |17.9511415440 |139.5419928061|5.9635961403 |
|80    |Hg     |5d106s2      |2.79|3   |5   |21 |21 |24 |858 |25 |25 |21 |29.5569517254 |6.9643863938  |3.7195391450 |
|81    |Tl     |5d106s26p1   |2.8 |3   |5   |27 |27 |15 |600 |21 |21 |33 |31.4741253336 |26.7796683701 |5.4771494988 |
|82    |Pb     |5d106s26p2   |2.4 |3   |7   |17 |17 |17 |165 |33 |33 |33 |31.9199528147 |39.6653333270 |5.6121469630 |
|83    |Bi     |6s26p3       |2.2 |2   |7   |21 |21 |7  |303 |25 |25 |75 |36.7170486278 |43.2917118072 |4.5469693595 |
|84    |Po     |6s26p4       |2.19|2   |7   |25 |25 |25 |455 |21 |21 |21 |37.5496026885 |45.7765857674 |4.9449696293 |
|86    |Rn     |6s26p6       |2.2 |2   |7   |12 |12 |12 |84  |45 |45 |45 |93.0786368157 |0.5240846518  |15.0092389360|

