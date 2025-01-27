if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <script_path>"
    exit 1
fi

# read script path from command line
EOS_script="$1"

if [ -f $EOS_script ]; then
  for i in 0.94  0.96  0.98  1.0  1.02  1.04  1.06
  do
  cd $i
  python '../'$EOS_script *95.onetep
  cd ../
  done
fi
