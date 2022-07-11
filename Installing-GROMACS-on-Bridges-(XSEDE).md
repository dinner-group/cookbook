DISCLAIMER: You can ignore this article if you are using GROMACS on Midway. This is only for installing midway on other clusters. 

If for any reason you need to install GROMACS yourself (i.e. for use on Bridges, an XSEDE resource), you should install GROMACS 2019.4 patched with Plumed 2.5.3, to match [Chatipat's installation on Midway](/display/thecookbook/GROMACS+2019.4+with+GPU+Support). This process can be a little arduous, as it intimately depends on the types of compilers you use, how recent those compilers are, and the version of mpi you use. You may need to play around with this quite a bit to get a version that passes all of the tests. You should absolutely become very familiar with both the [PLUMED installation guide](http://tcb.ucas.ac.cn/plumed2/user-doc/html/_installation.html) and the [GROMACS installation guide](http://manual.gromacs.org/documentation/2019.4/install-guide/index.html). Note that you will need to download the proper source code from their websites, and then upload it onto Bridges. Below is an example script that I used to install my GROMACS version on Bridges, as of January 2020. Again, you have to be very aware of the modules you have loaded, and the different compilers you are using. Be sure to explicitly unload anything you are not using, to prevent conflicts. Note that this **does not **have CUDA support, meaning it cannot be run on GPUs. There are more steps if you want CUDA support, which will not be covered here.

As a final note, if you do run into problems that you cannot solve (i.e. tests that you always fail and you cannot figure out why, compilations that always fail regardless of compilers used, etc.) you should feel free to post in the [PLUMED google group](https://groups.google.com/g/plumed-users) or the [GROMACS forum](https://gromacs.bioexcel.eu/). Both are great resources for questions you cannot find the answers to otherwise. Just be sure to read the rules before posting (and read to see if your question has been asked before), and be very descriptive in your question. 

PLUMED Installation
-------------------


    #Define the install and build directories
    BUILD_ROOT="/pylon5/mc5fphp/anto/gromacs_src”
    INSTALL_ROOT="$HOME/software/plumed_2.5.3"
    
    #Load the openmpi and fftw3 modules
    module load mpi/gcc_openmpi
    module load fftw3

    #Open the package
    tar -xzf "plumed2-2.5.3.tar.gz"
    cd plumed2-2.5.3
    
    #Configure and make
    ./configure CXX=mpicxx CC=mpicc FC=mpifort --prefix=${INSTALL_ROOT}
    make -j8
    
    #These paths will be needed both for the installation and for GROMACS
    source “sourceme.sh”
    
    #This can sometimes be testy. Stick with it, and post in the PLUMED mailing list if you can’t figure it out.
    #Using intel normal compilers and gcc_openmpi worked for me - intel_openmpi optimized too much, and
    #made it so 10 tests were failed in this step.
    #Make sure you are completely unloading any compilers/mpi versions that you are not using
    make check -j8
    
    #If the check passes, then install and copy the module file into your own module file, so that you can use the module manager to load plumed
    make install
    cp ${INSTALL_ROOT}/lib/plumed/modulefile ${INSTALL_ROOT}/../modules/plumed_2.5.3

  

GROMACS Installation
--------------------
    
    #Note the version of openmpi and gcc that I used - this is also very finniky. Intel never really worked,
    #and only older versions of gcc worked. Gcc 10.1, the default, certainly did not work
    #Again, you have to be very careful to explicitly unload any compilers/mpi versions you are not using
    cd $BUILD_ROOT
    module load cmake
    module load mpi/gcc_openmpi
    module load gcc/4.8.4
    
    #Open the files and set the install directory
    INSTALL_ROOT="$HOME/software/gromacs_2019.4”
    tar -xzf “gromacs_2019.4.tar.gz"
    tar -xzf “regressiontests-2019.4.tar.gz”
    cd gromacs_2019.4

    #Patch GROMACS w/PLUMED
    plumed-patch -p -e "gromacs-2019.4"
    mkdir build-gromacs
    cd build-gromacs
    
    #Write the CMAKE command
    cmake .. \
     -DCMAKE_C_COMPILER=mpicc \
     -DCMAKE_CXX_COMPILER=mpicxx \
     -DGMX_MPI=ON \
     -DCMAKE_INSTALL_PREFIX="${INSTALL_ROOT}" \
     -DGMX_BUILD_OWN_FFTW=OFF \
     -DGMX_FFT_LIBRARY=fftw3 \
     -DREGRESSIONTEST_PATH="${BUILD_ROOT}/regressiontests-2019.4" \
     -DGMX_SIMD=AVX2_256
    
    #Make the installation, and check to make sure it's correct
    #Upon running ‘make check’, I pass 47/48 tests. The only test I fail is the HardwareUnitTests, specifically the HardwareTopologyTest.
    #I asked the GROMACS mailing list what gives, and they told me it was fine, and indeed that error is entirely benign with 2019.
    #I could also have thrown in -DGMX_HWLOC=off into the cmake command and would have passed all of the tests upon make check
    
    make -j8
    make -j8 check
    
    #Install
    make install

Use
---

You might want to define an easily callable script that explicitly loads all the modules you need, loads the right compilers, and loads GROMACS itself. In my .bashrc file, I have the command `mlg` aliased so that it calls the following script. 


    #Load my version of python
    export PATH="/pylon5/mc5fphp/anto/anaconda3/bin:$PATH"
    
    #This is a necessary variable to have set for correct job placement using sbatch on bridges
    export I_MPI_JOB_RESPECT_PROCESS_PLACEMENT=0
    
    #Add the GROMACS path
    export PATH="${HOME}/software/gromacs_2019.4/bin:$PATH"
    
    #Unload/load the correct modules
    module use $HOME/software/modules
    module unload intel
    module load plumed_2.5.3
    module load mpi/gcc_openmpi
    
    #Load GROMACS
    . "${HOME}/software/gromacs_2019.4/bin/GMXRC"
    
    #Make it so PLUMED and GROMACS can both back up files near-indefinitely. For some reason, these caps are by default low, which can cause some problems
    #when you are consistently overwriting files.
    
    export PLUMED_MAXBACKUP=10000
    export GMX_MAX_BACKUP=-1