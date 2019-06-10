for i in {15..19}
do
  bash /Applications/MATLAB_R2016a.app/bin/matlab -nodisplay -nodesktop < mat2csv$i.m &> dumpDots$i.log&
  process_id=$!
  wait $process_id
  echo "dump dots $i done"
done
git status
