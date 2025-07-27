# Analyse module
Run the following command to analyse the results.

```
for i in $(ls -d */)
do
name=$(echo $i | awk -F'/' '{print $1}')
cd $name

# get number of atoms
num_atoms=$(grep "Totals" 1.0/*.onetep | awk '{print $2}')
edft=$(grep "edft" 1.0/*.dat|awk '{print $3}')
# get delta
bash get_EOS.sh get_EOS.py > EOS.dat
python delta.py EOS.dat $edft $name $num_atoms

cd ../
done
```

