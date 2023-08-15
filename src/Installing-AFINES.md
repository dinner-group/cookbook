# Installing-AFINES.md
To install AFINES, you will need _git_, _make_, a _C++11 compiler_, and _boost_.

Downloading and compiling AFINES can be done as follows:

    git clone https://github.com/Simfreed/AFINES
    cd AFINES
    git checkout master  # or any other branch you want
    make network

If everything goes well, there should now be an AFINES binary at _bin/afines_.

Midway2
=======

*   Make sure that _gcc,_ _intel_, or any other compiler is **not** loaded using modules.  
    Running _which g++_ should give _/bin/g++_.
    
*   Make sure that _boost_ is **not** loaded using modules.  
    Running _echo $BOOST\_ROOT_ should give a blank line.

Python Bindings
===============

The Python bindings for AFINES are currently not mature and severely undocumented. However, as far as I (Chatipat) can tell, they appear to work properly. In addition to the usual dependencies, the Python bindings require _cmake_ and a working installation of _Python 2.7 or 3.x_. **If you are on Midway, install your own Python using Anaconda.**

Downloading and compiling AFINES as a Python module can be done as follows:
    
    git clone https://github.com/Chatipat-and-Steven-friendship-forever/AFINES.git
    cd AFINES
    git checkout chatipat_python
    git submodule update --init --recursive
    
    mkdir build
    cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release  # change to -DCMAKE_BUILD_TYPE=Debug for debugging
    
    make pyafines