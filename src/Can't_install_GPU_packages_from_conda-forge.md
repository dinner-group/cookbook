# Can't install GPU packages from conda-forge

Problem
-------
When installing or updating packages from the conda-forge channel, conda refuses to install the GPU version regardless of what's specified.

Solution
--------
Add `CONDA_OVERRIDE_CUDA=11.2` before the conda command. For example,
```
CONDA_OVERRIDE_CUDA=11.2 conda install jax -c conda-forge
```
This problem occurs because conda makes a [virtual package](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-virtual.html) for the CUDA version it detects.

[source](https://conda-forge.org/blog/posts/2021-11-03-tensorflow-gpu/#installation)
