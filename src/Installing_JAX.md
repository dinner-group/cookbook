# Installing JAX

In this guide, I'll describe how to install JAX with GPU support on Midway.
The official JAX installation guide is available [here](https://jax.readthedocs.io/en/latest/installation.html).
We'll install JAX using conda because it's the only reliable way I've found to get JAX to work with Beagle GPUs.
As JAX depends on very specific versions of other libraries, I recommend creating a new environment.

    conda create -n jax
    conda activate jax

We'll install packages from [conda-forge](https://conda-forge.org/).
Beagle doesn't have the right CUDA versions, so we'll also install cuda-nvcc from the nvidia channel.

    conda config --env --set channel_priority flexible
    conda config --env --add channels nvidia
    conda config --env --add channels conda-forge

The order of the last two commands is important.
The output of `conda config --show channels` should be:

    channels:
      - conda-forge
      - nvidia

We'll now install JAX packages.

    CONDA_OVERRIDE_CUDA=11.8 conda install jaxlib=*=*cuda* jax cuda-nvcc

Make sure that cuda-nvcc is installed from the nvidia channel (cuda-nvcc from the conda-forge channel doesn't work).
The output of `conda list cuda-nvcc` should contain nvidia in the channel column, for example:

    # Name                    Version                   Build  Channel
    cuda-nvcc                 12.4.131                      0    nvidia

Note that `CONDA_OVERRIDE_CUDA=11.8` should be put before every `conda install`, `conda update`, and `conda remove` command.
This is needed because conda will only install GPU packages if it detects GPUs, but Midway login nodes don't have GPUs.
You can now install other packages, for example:

    CONDA_OVERRIDE_CUDA=11.8 conda install flax optax orbax-checkpoint

Flax is the most popular neural network library for JAX.
Optax is the main gradient-based optimization library for JAX.
Orbax-checkpoint is a checkpoint library for JAX.
See [awesome JAX](https://github.com/n2cholas/awesome-jax) for an extensive list of JAX libraries.