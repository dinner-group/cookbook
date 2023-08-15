# [Midway]-Modules-need-to-be-repeatedly-loaded_unloaded-before-they-work-on-a-compute-node..md
Problem
-------

This is a partial solution to the need to repeatedly load/unload modules such as PLUMED and GROMACS before they start working on compute nodes.

Part of the problem comes from how SLURM sets up a job: the environment variables (run `env` to see the list of current environment variables) which are not related to SLURM are copied to a newly started process. The result is that `module` believes that the loaded modules are already set up, while in fact they are only partially set up.

Solution
--------

One way to prevent some of this problem from occurring is to not copy any environment variables related to `module` to the job. A side benefit is that submit scripts are now more reproducible since the environment is the same each time you submit.

To partially solve this:

1.  Remove all traces of `module` from your `.bashrc` file.
2.  Add `#SBATCH --export=NONE` to your submit script. What this does is instead of copying the environment variables from the shell you're submitting the job from, it starts a new shell (`.bashrc`  will be sourced) and copies the environment variables from that. Note that you'll have to all `--export=ALL` to any `srun` commands you call in your submit script if you want environment variables to be passed on.
