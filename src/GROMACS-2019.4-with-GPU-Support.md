# GROMACS-2019.4-with-GPU-Support.md
As described [Running Jobs on Midway](/display/thecookbook/Running+Jobs+on+Midway), GROMACS 2019.4 patched with PLUMED 2.5.3 with CUDA 10.0 support has been installed on Midway. To load this module, run the following bash command:

```
source /project2/dinner/gromacs/sourceme.sh
```

GROMACS can now be run using _gmx\_mpi_. More information on running/analyzing molecular dynamics simulations on Midway can be found at [Molecular Dynamics Essentials](/display/thecookbook/Molecular+Dynamics+Essentials). 

This GROMACS installations comes with GPU support! In general, running MD on GPUs increases speed by around an order of magnitude. Our current GPU access is primarily through the GM4 cluster. Here are benchmarks of insulin on the GM4 cluster.

For CPUs, using 2 OpenMP threads appears to be fastest. The speed benefit isn't that large compared to using all MPI processes, though.

For GPUs, the overhead of using MPI is rather high. Using all OpenMP threads is the fastest.

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
| #Processors | **#MPI Processes** | **#OpenMP Threads** | **Speed (ns/day)** |     |
| **No GPUs** | **1 GPU** |
| 1   | 1   | 1   | **1.757** | **41.557** |
| 2   | 1   | 2   | 3.526 | **65.580** |
| 2   | 1   | **3.528** | 33.459 |
| 4   | 1   | 4   | 6.431 | **96.643** |
| 2   | 2   | **6.720** | 55.185 |
| 4   | 1   | 6.681 | 57.418 |
| 8   | 1   | 8   | 13.695 | **126.284** |
| 2   | 4   | 12.134 | 77.221 |
| 4   | 2   | **15.888** | 81.082 |
| 8   | 1   | 14.071 | 66.851 |