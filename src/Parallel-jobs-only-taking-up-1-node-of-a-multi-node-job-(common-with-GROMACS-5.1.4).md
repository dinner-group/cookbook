# Parallel-jobs-only-taking-up-1-node-of-a-multi-node-job-(common-with-GROMACS-5.1.4).md
Problem
-------

If you have one master job that separates out specific tasks using `mpirun`, you normally will want those jobs to all run on different cores, so that they don't interfere with one another. For example, let's say I requested a 4 node job that requests 4\*28 = 112 cores. I want this job to run 56 simulations that each take up two cores. If you run 56 iterations of '`mpirun -np 2 ... &` ' SLURM should, by default, determine which cores are not already on use and put your jobs on those cores, automatically distributing your 56 simulations in parallel evenly across all 112 cores. However, sometimes, either because RCC has updated SLURM to break compatibility with certain softwares (specifically, GROMACS 5.1.4), or just because the Midway gremlins are angry at you, this behavior doesn't actually work. In this case, what SLURM will instead do is try to schedule all of your jobs on just _one _node, not realizing that it might already be full. This could lead to some odd/slow behavior where jobs are not running in parallel as you would like them to. To confirm this, you can always `ssh` into a particular node you are running a job on ( `ssh midway2-0642`, for example), and then run `top` to see what is currently running. 

Solution
--------

You can explicitly bind certain jobs to certain nodes by passing the name of the desired node to `mpirun` using the `--host `flag . There are multiple ways to do get the hostnames for a certain job, below is just one solution:


    #Assume we have a 2 node (56 core) job, and we want to run two GROMACS simulations, one on each node
    
    #Use scontrol to get the list of nodes for your current job from SLURM
    
    hostlist=$(scontrol show hostname)
    
    #Convert that node list into an indexed array
    
    read -ra hostarr <<< $hostlist
    
    #Choose the specific nodes you want to run on
    
    host_nm0=${hostarr[0]}
    
    host_nm1=${hostarr[1]}
    
    #Run one GROMACS job on the first node, and run the other on the second node
    
    mpirun -np 28 --host ${host_nm0} gmx_mpi mdrun -v -plumed plumed.dat -ntomp 1 -deffnm test0 &
    
    mpirun -np 28 --host ${host_nm1} gmx_mpi mdrun -v -plumed plumed.dat -ntomp 1 -deffnm test1 &

