for i in {1..5}
do
  bash /Applications/MATLAB_R2016a.app/bin/matlab -nodisplay -nodesktop < mat2csv.m &> dumpCSV$i.log&
  process_id=$!
  wait $process_id
  echo "dump dots $i done"
done