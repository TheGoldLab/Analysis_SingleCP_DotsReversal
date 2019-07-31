#!/bin/bash
while read p; do
  echo "$p"
  sed -i.bak "s/timestamp=..................;/timestamp='$p';/" mat2csv.m 
  bash /Applications/MATLAB_R2016a.app/bin/matlab -nodisplay -nodesktop < mat2csv.m &> dump8CSV$p.log&
  process_id=$!
  wait $process_id
  echo "$p" >> dumped.txt
done <todump.txt
