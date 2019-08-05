#!/bin/bash
while read p; do
  echo "$p"
  sed -i.bak "s/timestamp=..................;/timestamp='$p';/" customFIRA.m 
  bash /Applications/MATLAB_R2016a.app/bin/matlab -nodisplay -nodesktop < customFIRA.m &> dump_customFIRA$p.log&
  process_id=$!
  wait $process_id
  echo "$p" >> dumped.txt
done <todump_customFIRA.txt
