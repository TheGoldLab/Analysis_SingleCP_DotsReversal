Aims of the branch reverse_corr:

My main worry is that the random seed be trustworthy.

Regarding the dots stimulus:

1. write a script that displays the dots stimulus from a specific trial
2. write a trivial task with a single trial and check that the dots 
from the task and the dots from the copycat script are identical 
(for this, use slow speed and few dots)  
3. write a script that dumps the dots stimulus from a specific trial into a 3D matrix
4. incorporate the dumping step into the task code itself; then reproduce
step 2, but comparing the matrices instead of the actual visual stimulus.
5. write a script that produces the dots stimulus corresponding to a given 
matrix
6. Once the mapping dots stimulus <-> 3D matrix is clear, safe and established,
write script that computes motion energy.
7. Make sure that the motion energy script measures what it is meant
to measure.
