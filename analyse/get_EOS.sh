if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <script_path>"
    exit 1
fi

# read script path from command line
EOS_script="$1"

if [ ! -f "$EOS_script" ]; then
  echo "ERROR: $EOS_script not found" >&2
  exit 1
fi

for i in 0.94  0.96  0.98  1.0  1.02  1.04  1.06
do
if [ ! -f "$i/log" ]; then
  echo "ERROR: $i/log not found" >&2
  exit 1
fi
cd "$i"
python '../'$EOS_script log
status=$?
cd ../
if [ "$status" -ne 0 ]; then
  echo "ERROR: $EOS_script failed for volume $i" >&2
  exit 1
fi
done
