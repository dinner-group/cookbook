Problem
-------
Sometimes the sbatch file does not like when you put multiple`mpirun -np 1`commands in the same file. I truly do not know why this is, as it should be fine. However, sometimes when I try to do it, nothing happens upon the second call to`mpirun`\- no errors or messages of any kind, just nothing.  The first simulation is running in the background, but the second simulation is not processed until the first one completes. 

Solution
--------

This strange behavior seems to go away when you just remove the`mpirun`entirely, and start with`gmx_mpi`. When`mpirun`isn't present, GROMACS assumed an implicit`mpirun -n 1.`Again, I truly don't know why it would make any difference, whether the call is explicit or implicit, but it fixed my problems. Just so you know. 
