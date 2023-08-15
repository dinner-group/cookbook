# Run-Gromacs-on-the-GM4-Cluster.md
The architecture and use of the gm4 partition is described in [Running Jobs on Midway](/display/thecookbook/Running+Jobs+on+Midway). Note that each user is only allowed to simultaneously submit 28 jobs to the gm4 partition. For MD, this means that you cannot submit a large array job to run many short simulations in parallel. Instead, you can run a shorter number of longer simulations, or manually manipulate your 28 gm4 jobs to submit many simulations. 

Below is an example sbatch file to run 4 parallel Gromacs simulations on a GM4 node, each with 10 CPUs and 1 GPU.

    #!/bin/bash
    #SBATCH --account=pi-dinner
    #SBATCH --partition=gm4
    #SBATCH --qos=gm4
    #SBATCH --nodes=1
    #SBATCH --ntasks=4
    #SBATCH --cpus-per-task=10
    #SBATCH --mem-per-cpu=2G
    #SBATCH --gres=gpu:4

    export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
    source /project2/dinner/gromacs/sourceme.sh

    # run 4 different simulations, each with 1 gpu and 10 cpus
    # gromacs is most efficient with 1 mpi rank per gpu and many openmp threads
    # gpus are numbered from 0-3
    # gpu_id tells which gpus to use

    mpirun -n 1 gmx_mpi mdrun -ntomp 10 -gpu_id 0 &
    mpirun -n 1 gmx_mpi mdrun -ntomp 10 -gpu_id 1 &
    mpirun -n 1 gmx_mpi mdrun -ntomp 10 -gpu_id 2 &
    mpirun -n 1 gmx_mpi mdrun -ntomp 10 -gpu_id 3 &

    wait

  

Note the _&_ (telling the bash process to run in the background) and the _wait_ statement (telling bash to only move on once all background tasks are complete). If you are just running one simulation, you need neither of these things. 

Also note that the #SBATCH `--gres=gpu:4` flag is requesting 4 GPUs _per node_, as opposed to 4 GPUs overall.

**Regarding the presence of `mpirun -np 1` :** for some reason, and I truly have no idea why this would be, sometimes the sbatch file does not like when you put multiple `mpirun -np 1` commands in the same file. I truly do not know why this is, as it should be fine. However, sometimes when I try to do it, nothing happens upon the second call to `mpirun` - no errors or messages of any kind, just nothing.  The first simulation is running in the background, but the second simulation is not processed until the first one completes. This strange behavior seems to go away when you just remove the `mpirun` entirely, and start with `gmx_mpi`. When `mpirun` isn't present, GROMACS assumed an implicit `mpirun -n 1.` Again, I truly don't know why it would make any difference, whether the call is explicit or implicit, but it fixed my problems. Just so you know. 

Finally, you can change the `--mem-per-cpu` flag to fit your needs. Check out [Running Jobs on Midway](/display/thecookbook/Running+Jobs+on+Midway) for node/memory descriptions for various partitions, and choose accordingly.