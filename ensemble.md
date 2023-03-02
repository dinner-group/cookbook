# Ensemble jobs on Midway

Oftentimes, you find yourself having to do the same task over and over again with very minor tweaks—for example processing a series of output files, or running the same script on a bunch of input files.
In these cases, it is advantageous to take advantage of tools that let you run these _embarrassingly parallel_ tasks at the same time.
There are two main ways of doing this: `gnu parallel` and job arrays.
GNU parallel is better suited to short (think <5 minutes) and non-resource intenstive tasks. Job arrays are better suited for longer-running tasks.

## Parallel Batch Jobs

You can use the `gnu parallel` utility to run multiple unconnected tasks at once on the same node (or across nodes). The [guide](https://rcc-uchicago.github.io/user-guide/midway23/examples/example_job_scripts/#parallel-batch-jobs) on the RCC website (and this [website](https://sulis-hpc.github.io/advanced/ensemble/gnuparallel.html)) is quite helpful for figuring out how to do this. Here's an example for running a Python script for a whole bunch of input files in parallel:

```
#!/bin/sh
#SBATCH --job-name=load-frames
#SBATCH --output=load-frames.out
#SBATCH --error=load-frames.err
#SBATCH --partition=dinner
#SBATCH --account=pi-dinner
#SBATCH --qos=dinner
 
#SBATCH --time=48:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=48
#SBATCH --mem-per-cpu=16G
 
# NOTE DO NOT USE THE --mem= OPTION
 
source ~/.zshrc
 
module load vmd
conda activate /project/dinner/scguo/anaconda3/envs/py39
 
# Load the default version of GNU parallel.
module load parallel
 
# When running a large number of tasks simultaneously, it may be
# necessary to increase the user process limit.
ulimit -u 10000
 
# This specifies the options used to run srun. The "-N1 -n1" options are
# used to allocates a single core to each task.
srun="srun --exclusive -N1 -n1"
 
# This specifies the options used to run GNU parallel:
#
#   --delay of 0.2 prevents overloading the controlling node.
#
#   -j is the number of tasks run simultaneously.
#
#   The combination of --joblog and --resume create a task log that
#   can be used to monitor progress.
parallel="parallel --delay 0.2 -j $SLURM_NTASKS --joblog runtask.log"
 
echo "  started at `date`"
topfile="/project/dinner/scguo/ci-vsd/models/MD-clustering-center/civsd.psf"
echo $topfile
echo $(which python)
script="/project/dinner/scguo/ci-vsd/python/load_frames.py"
 
# run the script for every file q_X_Y.txt where X runs from 2-8 and Y runs from 0-9 (inclusive)
$parallel "$srun python $script q_{1}_{2}.txt $topfile q{1}{2}.xtc" ::: {2..8} ::: {0..9}
 
echo "  finished at `date`"
```

## Job arrays

If each task is somewhat more resource intensive, it might make sense to group your jobs together using a _job array_ which basically assigns a "parent" job that has a bunch of children who do the same thing but with slightly different parameters you specify.
Some good examples of how to set this up are [here](https://sulis-hpc.github.io/advanced/ensemble/jobarrays.html).

Here's an example script for running a lot of short MD simulations:
```
#!/bin/bash
#SBATCH --job-name=aib9

#SBATCH --partition=beagle3
#SBATCH --account=pi-dinner
#SBATCH --qos=beagle3

#SBATCH --nodes=1           # these resource specifications are
#SBATCH --ntasks=1          # all *per* task
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --constraint=a40
#SBATCH --mem=1G
#SBATCH --array=0-690       # here you specify the range of numbers

#SBATCH --time=1:00:00

source ~/.zshrc
conda activate openmm

jobindex=$SLURM_ARRAY_TASK_ID # this number will refer to the array number

# do some math to figure out which file to run
parentindex=$((jobindex / 100))
childindex=$jobindex

home_dir="/project/dinner/scguo/aib9"
workdir="$home_dir/$parentindex/$childindex"
parm="$workdir/system_hmass.prmtop"

n_steps=5000000 # 5_000_000 * 0.004 ps = 20,000 ps = 20 ns
save_int=250 # 250 * 0.004 ps = 1 ps
coord="$workdir/system.mdcrd"

# run 10 copies of each starting coordinate
for iteration in {0..9}; do
    echo "Running iteration $iteration for $workdir"
    # runs a short simulation in OpenMM for a given starting coordinate file
    python run.py $coord $parm -t $n_steps -s $save_int -p cuda -d $workdir -o $iteration
done
```