# Notes-on-Midway-Modules.md
These are my notes on the state of modules on Midway.

General Notes
=============

Modules on the login nodes, the broadwl nodes, the weare-dinner2 nodes, and the gm4 nodes are the same.

Most of module contents are contained in /software. These also typically contain the compilation log, although the build scripts are hidden in the accounts of the RCC people.

A module _name_/_version_ is usually contained in /software/_name_\-_version_\-el7-x86\_64/

A module _name_/_version_+_compiler_ is usually contained in /software/_name_\-_version_\-el7-x86\_64+_compiler_/

Compilation
===========

Compiling C/C++/fortran codes on midway2 can be very painful if you're using MPI, OpenMP, or GPUs. The easiest, although not that well performing, method is to use Anaconda's gcc, mpich, and cudatoolkit.

The default gcc compiler is gcc 4.8.5, which is not in a module. The following C/C++/Fortran compilers are available:

*   clang 3.8.0, 3.9(default), 7.1.0+gcc-6.1
*   gcc 4.4.7, 6.1(default), 6.2, 6.3.0, 7.2.0, 8.2.0, 9.1.0, 9.2.0
*   intel 12.1, 15.0, 16.0(default), intel 17.0, 18.0, 18.0.5, 19.0.1
*   pgi 2016, 2017(default)

The latest versions of gcc and intel compilers usually give the fastest code. The pgi compiler gives junk code for gromacs (wrong results). clang/7.1.0+gcc-6.1 will also load gcc/6.1.

When using newer intel compilers than the default, you may need to load gcc also, since the intel compiler uses gcc's libraries. gcc/6.1 seems fine when that's needed.

gcc 9.2.0, 8.2.0, 7.2.0, 6.3.0, 4.4.7 have threads disabled. This means that you can't compile software to use more than one thread (core). This includes OpenMP, pthreads, Intel TBB. Note that software that runs multiple copies of the same program and communicates between them, such as MPI, and software that uses libraries which internally uses threads, such as MKL, won't be affected.

MPI libraries are either compiled with the default compiler (gcc 4.8.5) or with another compiler, indicated after the "+". If the MPI implementation is compiled with a non-default compiler, loading the module will also load the associated compiler. The following MPI implementations are available:

*   intelmpi 4.0+intel-12.1, 5.0+intel-15.0, 5.1+intel-16.0(default), 2017.up4+intel-17.0, 2018.2.199+intel-18.0, 2018.4.274+intel-18.0.5
*   mpich 3.2(default)
*   mvapich2 2.2(default)
*   openmpi 1.10+intel-16.0, 1.10+pgi-2016, 1.6, 1.6+intel-12.1, 1.8, 2.0+intel-16.0, 2.0.1(default), 2.0.2, 2.0.2+gcc-6.2, 3.0.0, 3.0.0+gcc-6.2, 3.0.0+gcc-7.2.0, 3.1.2

When running an MPI application, mpirun seems to work much more reliably than srun, which breaks whenever they update SLURM.

openmpi/3.0.0+gcc-7.2.0 doesn't work for me. It gives the error: "WARNING: There was an error initializing an OpenFabrics device."  
openmpi seems to have trouble with the gm4 cluster. There are two infiniband ports on the gm4 cluster, one of which is disabled. openmpi tries to use the disabled one.

In my hands, mpich and mvapich2 seem to not want to run multiple processes with srun. I think it's because it's compiled against the wrong version of slurm. What it does instead is run multiple copies of the same process (ex. `srun -n 2 gmx_mpi mdrun` runs 2 copies of the same simulation instead of one simulation on 2 cpus). mpich still works if you call mpirun directly. mvapich2 doesn't even have mpirun, so it's toast.

Intel mpi also doesn't seem to work with srun. It crashes. mpirun works fine.

CUDA versions available:

*   cuda 6.5(default), 7.5, 8.0, 9.0, 9.0a, 9.1, 10.0, 10.1
*   cudnn 7.5.0.56\_cuda10.0

CUDA compilers need specific versions of gcc or intel. The gm4 cluster uses Volta gpus, which require cuda >= 9.0.

cuda/9.0, cuda/9.0a, and cuda/9.1 need the gcc 4.8.5 (no modules) or intel/17.0  
cuda/10.0 needs gcc 4.8.5 (no modules), intel/18.0, or intel/18.0.5  
cuda/10.1 needs gcc 4.8.5 (no modules) or intel/19.0.1