for i in $(ls -d */ | awk -F/ '{print $1}') 
do 
cd $i 
for j in 0.94  0.96  0.98  1.0  1.02  1.04  1.06
do 
cd $j 
sed -i '$anum_kpars : 96' *.dat 
cd ../ 
done
cd ../
done
