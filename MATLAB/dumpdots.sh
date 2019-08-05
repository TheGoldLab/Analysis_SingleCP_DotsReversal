for i in {1..20}
do
  bash /Applications/MATLAB_R2016a.app/bin/matlab -nodisplay -nodesktop < mat2csv.m &> dump7CSV$i.log&
  process_id=$!
  wait $process_id
  echo "dump dots $i done"
done
