# [MD]-Mpiexec-error-prevents-simulations-from-running.md
Problem
-------

```
You get something that looks like the following error:mpiexec_hani-laptop: cannot connect to local mpd (/tmp/mpd2.console_hani); possible causes:
  1. no mpd is running on this host
  2. an mpd is running but was started without a "console" (-n option)
```

Solution
--------

You did not start your command with _mpirun,_ and you needed to. Rerun the command using _mpirun_. For example,`mpirun -np 4 gmx\_mpi mdrun -v -deffnm TEST`
