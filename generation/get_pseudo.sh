if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <pseudo_dir>"
    exit 1
fi

# read pseudo_dir from command line
pseudo_dir="$1"

if [ -d $pseudo_dir ]; then
  for i in $(ls -d */ | awk -F/ '{print $1}')
  do
  cp $pseudo_dir/$i\_* $i
  done

  for i in $(ls -d */ | awk -F/ '{print $1}')
  do
  cd $i
  for j in 0.94  0.96  0.98  1.0  1.02  1.04  1.06
  do
  cp $i\_* $j
  done
  cd ../
  done
fi
