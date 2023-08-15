# Running Jobs on Midway
Useful Commands
===============

It might be useful to explore the following commands to see all of the partitions, SUs, and data storage options that are available to you. 

`rcchelp qos` — available partitions and job limits

`rcchelp squeue` — jobs you have running

`squeue -p <partition_name>` — all jobs running on partition

`rcchelp quota` — file usage limits

`scontrol` — specific details about jobs, partitions, nodes, etc.

`sinfo -p <partition_name>` — how many nodes are available on partition

`module list` — the modules currently loaded/accessible to you

`module avail `— all modules made available by RCC. You can look for a specific software with `module avail <software>`. You can load/unload a specific module with `module load <software>` or `module unload <software>`

`rcchelp balance` — how many SUs we have left

`rcchelp usage` — how many SUs you've used

More information on modules on Midway can be found in [Notes on Midway Modules](/display/thecookbook/Notes+on+Midway+Modules). In the next sections, I will describe how to take advantage of the above resources by using the SLURM job scheduler. 


Other useful information about submitting jobs using SLURM is found at this [website](https://vsoch.github.io/lessons/sherlock-jobs/) from Stanford.

Interactive Job
--------------

An interactive job gives you a terminal on a compute node that you can type commands into. You can request an interactive job using the `sinteractive` command. Note that you'll have to wait for a bit until the compute nodes are free enough to give you an allocation.

For example, to request a 3-hour long interactive job on the `dinner` partition (on Midway3) with 48 MPI processes and 48 \* 2 GB = 96 GB of memory, 

```
sinteractive --time=3:00:00 --partition=dinner --account=pi-dinner --qos=dinner --nodes=1 --ntasks=48 --cpus-per-task=1 --mem-per-cpu=2G
```

Note that the flag `--mem=96G` would request the same amount of total memory.

Batch Job
---------

A batch job will run a bash script some time in the future. Here is an example of a Midway2 sbatch script.

```
#!/bin/bash
 
#SBATCH --job-name=myjob        # the name appearing in squeue
#SBATCH --output=myjob.out      # output to STDOUT
#SBATCH --error=myjob.err       # output to STDERR
 
#SBATCH --time=6:00:00
 
#SBATCH --partition=dinner
#SBATCH --account=pi-dinner
#SBATCH --qos=dinner
 
#SBATCH --nodes=1
#SBATCH --ntasks=48
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
 
#SBATCH --export=NONE
 
#Load GROMACS
module load gromacs
 
#Example MD commands - notice the use of mpirun to run multi-core simulations
gmx_mpi grompp #fill in arguments
mpirun -n 28 gmx_mpi mdrun -ntomp #fill in arguments
```

Note that you use _mpirun_ to explicitly allocate multiple cores to a specific task. 

Midway3 Partitions
==================

caslake
-------

This partition is accessible to everyone on Midway3. However, currently queue times are still almost instantaneous (due to the slow adoption of Midway3 across PSD). Each caslake node has 48 processors and 180G of usable memory (anything above _\--mem=180G_ will return an error). The maximum run time allowed is 1.5 days (1-12:00:00). We are charged SUs for using these nodes, by the formula: max(#cpus, mem/4000MB) \* time/hr. To use these nodes, edit your sbatch script to include the following:

```
#SBATCH --partition=caslake
#SBATCH --account=pi-dinner
```

dinner
------

These nodes are only used by the dinner group. There are 8 dinner nodes, each with 48 processors and 375G of usable memory (anything above _\--mem=375G_ will return an error). The maximum run time allowed is 2 days (2-00:00:00) on the `dinner` qos. We aren't charged SUs for using them. However, keep in mind that these resources are shared across the entire group, and currently are heavily used. It is good practice to make sure there are at least a few nodes available at any given time. If you want to use a significant portion of these resources, you need to ask the other users if it is OK to hog the space. A good rule of thumb is to try to use less than 2 or 3 full nodes at any given time.  To run a job on these nodes, edit your sbatch script to include the following:

```
#SBATCH --partition=dinner
#SBATCH --account=pi-dinner
```

dinner-hm
---------

This node is only used by the dinner group. There is 1 dinner-hm node, where -hm stands for high memory. It has 48 processors and 1500G of usable memory (anything above _\--mem=1500G_ will return an error). The maximum run time allowed is 2 days (2-00:00:00) on the `dinner` qos. We aren't charged SUs for using this node, and it is most useful for very memory-intensive applications. To run a job on this node, edit your sbatch script to include the following:

```
#SBATCH --partition=dinner-hm
#SBATCH --account=pi-dinner
#SBATCH --qos=dinner
```

beagle3
-------

These nodes are shared by multiple groups. There are 44 nodes with GPUs, and 4 high-memory CPU-only nodes. Each GPU node has 32 processors, 250G of usable memory, and for the GPU nodes, and 4 GPUs (either Nvidia A100 or Nvidia A40). The maximum run time allowed is 2 days (2-00:00:00) on the _beagle3_ qos, and 4 days (4-00:00:00) on the _beagle3-long_ qos. Per user, you are allowed to use 16 nodes at one time on the _beagle3_ qos, and 4 nodes at one time on the _beagle3-long_ qos. There are no group restrictions, unlike GM4 on Midway2. Queuing times for this partition are generally quite small. This partition is particularly useful for large-scale, production-level MD simulations and ML applications. To run a job on these nodes, edit your sbatch script to include the following:

```
#SBATCH --partition=beagle3
#SBATCH --account=pi-dinner
#SBATCH --qos=beagle3
##SBATCH --qos=beagle3-long        #only needed for long simulations
```

Midway2 Partitions
==================

broadwl
-------

This partition is accessible to everyone on Midway2, so often has a long queue. Each broadwl node has 28 processors and 57G of memory. The maximum run time allowed is 1.5 days (1-12:00:00). We are charged SUs for using these nodes, by the formula: max(#cpus, mem/2000MB) \* time/hr.

```
#SBATCH --partition=broadwl
#SBATCH --account=pi-dinner
```

weare-dinner1
-------------

There are 10 weare-dinner1 nodes, each with 16 processors and 32G of total memory. The maximum run time allowed is 3 days (3-00:00:00) if you are using the `weare-dinner` qos, and 6 days (6-00:00:00) if you are using the `weare-dinner-long` qos. Currently, two are down (midway 063 and midway 068), leaving us with 8 working nodes. These are older nodes, using the same architecture as the now-decommissioned sandyb partition. As a result, some software modules may not work on this partition. In general, these can be fairly buggy, but are technically available to you. As Aaron and Jon own these nodes, we aren't charged SUs for using them. To run a job on these nodes, add

```
#SBATCH --partition=weare-dinner1
#SBATCH --account=weare-dinner
#SBATCH --qos=weare-dinner
```

to your submit script.

weare-dinner2
-------------

There are 11 weare-dinner2 nodes, each with 28 processors and 57G of total memory. The maximum run time allowed is 3 days (3-00:00:00) if you are using the `weare-dinner` qos, and 6 days (6-00:00:00) if you are using the `weare-dinner-long` qos. These nodes are tightly coupled with InfiniBand. Currently, 1 (midway2-0475) is down, and two run slow (midway2-0476 and midway2-0480; for example, GROMACS simulations take twice as long to finish on these nodes compared to the other weare-dinner2 nodes), leaving us with 8 nodes working at full speed. As Aaron and Jon own these nodes, we aren't charged SUs for using them. However, keep in mind that these resources are shared across the entire group. It is good practice to make sure there are at least a few nodes available at any given time. If you want to use a significant portion of these resources, you need to ask the other users if it is OK to hog the space. A good rule of thumb is to try to use less than 2 or 3 full nodes at any given time.  To run a job on these nodes, add

```
#SBATCH --partition=weare-dinner2
#SBATCH --account=weare-dinner
#SBATCH --qos=weare-dinner
```

to your submit script. Again, please leave at least one node completely free in case someone urgently needs to run something.

gm4
---

We have access to 19 GPU nodes and 4 CPU-only nodes on the gm4 cluster. Each node has 40 processors, 184207M of memory (around 179G), and for the GPU nodes, also 4 Nvidia V100 GPUs. The maximum run time allowed is 1.5 days (1-12:00:00). Per user, you are allowed to submit a maximum of 28 jobs at one time. However, for the entire `pi-dinner` account, we are only allowed to submit 48 jobs at a time. Furthermore, for the entire `pi-dinner` account, we are only allowed to use 320 CPUS/32 GPUs (8 full nodes) simultaneously.  This is the same as the per-person restriction, meaning that one user could technically use 8 full nodes simultaneously. However, GPU work is becoming increasingly popular, so these account limits are actually fairly restrictive. In general, try to keep your total usage at any given time below 2 full nodes (8 jobs, 8 GPUs, 80 CPUs). If you need to use more, you must first let the other gm4 users in the group know how many resources you will be requesting and for how long (in the #gm4 channel on slack). If you want to run a job and the resources are currently taken, also let that chat know. We aren't charged SUs for these nodes. Note that these nodes are shared with many other groups, so they may be crowded at times. To run a job on a GPU node, add

```
#SBATCH --partition=gm4
#SBATCH --account=pi-dinner
#SBATCH --qos=gm4
```

Note that you'll also need to specify how many GPUs you want, i.e. for 2 GPUs,

```
#SBATCH --gres=gpu:2
```

Note that this flag is equivalent to `--gpus-per-node`. So the above command is requesting 2 GPUs per node requested. To run a job on a CPU-only node (which can help with queuing times if you don't need a GPU), add

```
#SBATCH --partition=gm4
#SBATCH --account=pi-dinner
#SBATCH --qos=gm4-cpu
```

Additional information can be found at [gm4.rcc.uchicago.edu](http://gm4.rcc.uchicago.edu).


Example Submit Scripts
======================

Multiple Nodes, Midway2
-----------------------

```
#!/bin/bash
 
#SBATCH --job-name=myjob
#SBATCH --output=myjob.out
#SBATCH --error=myjob.err
 
#SBATCH --time=6:00:00
 
#SBATCH --partition=weare-dinner2
#SBATCH --account=weare-dinner
#SBATCH --qos=weare-dinner
 
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=28
#SBATCH --mem=8G
 
#SBATCH --export=NONE
```

Single Node, GPUs, Midway3
--------------------------

```
#!/bin/bash
 
#SBATCH --job-name=myjob
#SBATCH --output=myjob.out
#SBATCH --error=myjob.err
 
#SBATCH --time=72:00:00
 
#SBATCH --partition=beagle3
#SBATCH --account=pi-dinner
#SBATCH --qos=beagle3-long
 
#SBATCH --nodes=1
#SBATCH --mem=250G
#SBATCH --gres=gpu:2
#SBATCH --export=NONE
```
  

Other Sbatch Directives
=======================

`Resources`
-----------

`--nodes=`_num_  
`--nodes=`_min_`-`_max  
_Schedule tasks on exactly _num_ nodes, or between _min_ and _max_ nodes (inclusive). If `--nodes` is not specified, SLURM will decide how many nodes to use.

`--ntasks=`_num_  
The number of tasks to launch. Each task may be allocated on a different node, however, all the cores in a task will be on a single node.

`--ntasks-per-node=`_num_  
If `--nodes` is specified, run _num_ tasks per node.  
If `--ntasks` is specified, or both `--nodes` and `--ntasks` are specified, run at most _num_ tasks per node. This is almost assuredly not what you want.

`--cpus-per-task`  
The number of cores to allocate for each task. By default, each task has a single core. The cores in a task will not be split across multiple nodes.

`--mem  
``--mem-per-cpu`  
Request `--mem` memory per node or `--mem-per-cpu` per core. These flags are mutually exclusive.  
`--mem` is useful when allocating a single task, or when allocating whole nodes.  
`--mem-per-cpu` is useful when allocating multiple tasks across an unknown number of nodes, or when manually parallelizing what would be an array job.

Other
-----

`--time` 

`--job-name`

`--array=`_array\_spec_

Run a job array. It's clearer by example. Here are what different _array\_spec_ will run:

*   `1-10` : 10 jobs with indices 1, 2, ..., 10
*   `1,2,5` : 3 jobs with indices 1, 2, 5
*   `1-3,5,8-10` : 7 jobs with indices 1, 2, 3, 5, 8, 9, 10

In addition, you can specify how many jobs are allowed to run at a time by appending `%`_number_. For example, `1-10%3` will submit 10 jobs, but only allow 3 of them to run at a time.

The index can be accessed by the environment variable `$SLURM_ARRAY_TASK_ID` .

`--dependency`

Only run the job after the completion of another job (useful for building pipelines of jobs). For example, if I wanted to run a new job after job number $JOBID ends (either successfully or unsuccessfully), I could add the following dependency flag: _\--dependency=afterany:$JOBID_

`--mail-type`   
`--mail-user` 

`--chdir  
`By default, SLURM will run the submit script in the directory you submitted it from. This flag changes that directory.

`--export=NONE  
`By default, when you submit a job, SLURM will copy your current environment and load it before running commands in the submit script. With `--export=None`, SLURM will instead open a new bash process, copy its environment (`.bashrc` is run), and load that environment instead.

`--output  
``--error`  
Redirect stdout and stderr to the files named instead of letting using `slurm-${SLURM_JOB_ID}.out` and `slurm-${SLURM_JOB_ID}.err`.

`--exclusive `— evil flag. **DO NOT USE** unless you know what you're doing.  
This gives you the same amount of resources that you requested but doesn't allow anyone else to share the nodes you use. For instance, if you ask for 1 core and 2 GB of memory on broadwl, you will get 1 core and 2 GB of memory but will for charged for the whole node: 28 cores and 57 GB of memory. This will cost 28.5 times the number of SUs you actually needed. The only time this flag is ever useful is when you are allocating an entire node, and want to make sure that even if you didn't allocate all the resources in the node, no other jobs can use it.

`--exclude`\=_nodelist_  
Don't schedule jobs on certain nodes specified in _nodelist_. _nodelist_ is a comma-separated list of nodes, ex. `midway2-0476,midway2-0480` ; note that no spaces are allowed.

`--nice=`_nice_  
Decreases the priority of your job. A job with a higher _nice_ will run only after all jobs with a lower _nice_ are run. For example, a job with _nice=200_ will run after a job with _nice=100_, which in turn will run after a job with no _nice_ specified.

Software
========

gromacs
-------

On Midway2, we use a custom-installed version of GROMACS, which is GROMACS 2019.4 patched with PLUMED 2.5.3, with CUDA 10.0 support. This is slightly faster, is actively maintained, and can be used on gpu partitions. To load this GROMACS/PLUMED version, use the below command:

```
source /project2/dinner/gromacs/sourceme.sh
```

Chatipat Lorpaiboon kindly asks that you not break this installation!

For MD on Midway3, we have been using the default installed GROMACS 2020.4 patched with PLUMED 2.7 (_module load gromacs)._ The GPU performance on Midway3 still needs to be benchmarked.

Using either the above, one can now use GROMACS by using _gmx\_mpi_. For more information on the GROMACS installation, see [GROMACS 2019.4 with GPU Support](/display/thecookbook/GROMACS+2019.4+with+GPU+Support). For more information on running/analyzing molecular dynamics simulations on Midway, see [Molecular Dynamics Essentials](/display/thecookbook/Molecular+Dynamics+Essentials).