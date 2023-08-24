# Python
_Work in progress, Chatipat will write more eventually. Feel free to edit._

We use _Python_ for most of our data analysis.

Installation
============

Regardless of whether you are using Python on your local machine or on some cluster (Midway, Bridges, etc.) you should be using python3 (sorry, Bo). For installation on your local machine, you should download the [appropriate installer for mamba](https://mamba.readthedocs.io/en/latest/mamba-installation.html), which is a particularly useful Python environment manager that allows for easy an flexible installation of both python itself and, more importantly, any additional packages you may want to install later. It acts as a drop-in replacement for Anaconda which is incredibly slow and bulky (not recommended). Keep in mind that, especially as you install more packages, your installation can get quite bulky, both in terms of total storage space required and in the number of files saved. It is probably a good idea to periodically clean house. As far as usage, you can either work with raw python scripts, or various IDEs like Spyder or Jupyter Notebooks. The decision here is up to you, and is likely dependent on whatever individual task you are interested in. Jupyter Notebooks have become increasingly popular in the group, especially recently. 


If using Python on Midway, the best option is to install your own copy of mamba on Midway, and create environments for different versions of Python you need (e.g. Python 3.9, 3.11, etc.).
The preloaded versions on Midway are generally to be avoided.
You can download (or `curl`) the Linux installer from [here](https://github.com/conda-forge/miniforge#mambaforge), use` scp` to move it to Midway (your `/project/dinner/${USERNAME}/` directory is likely the best location). You should export the correct path to make sure you are using your newly-installed version of python, and not Midway's default version. It is possible that this installation breaks ThinLinc when you try to log into Midway in the future, likely because the installation [messed with your .bashrc file](./Make-a-Useful-.bashrc-file.md) in a not-so-cool way. You can fix that by [following these directions](./ThinLinc-stops-working-after-installing-Anaconda.md). 

Generally Useful Libraries
==========================

NumPy
-----
See [below](#numpy-1).

SciPy
-----
Important scientific programming package with useful functions for performing linear algebra routines, optimization, and much more.

matplotlib
----------
Good for plotting and [making figures](./Figure-Creation.md).
Best combined with other packages such as `seaborn`.

scikit-learn
------------
Package with **many** machine learning tools, such as clustering, regression, cross-validation, and more.

Optimization
============

The features that make Python so convenient to write also make it quite slow. Fortunately, there are several libraries that can help you speed up your code without resorting to coding in a more unpleasant programming language.

NumPy
-----

If you aren't using NumPy for your numerical calculations, you're doing it wrong. NumPy relies on _vectorization_ to speed up your code. Basically, it avoids the overhead of Python by doing _large chunks of work_.

Numba
-----

Numba takes a subset of Python code and makes it run faster. It is useful for numerical, loop-heavy code that you would typically write in a low-level language.

Jax
---
[Jax](https://jax.readthedocs.io/en/latest/#) is a library which combines vectorization, just-in-time compilation (including on GPUs!) and autograd. It's primarily used in machine learning contexts for the autograd capabilities, but it has the great benefit of also being able to compile high-level Python code (unlike Numba, which mostly only works for numerical methods) for high performance.

Parallelization and Concurrency
===============================

multiprocessing
---------------

multiprocessing runs Python on another CPU.

Joblib
------

Joblib is a very easy way of running _embarassingly parallel_ Python code on multiple CPUs. It is also useful for _pipelines_, where you set up a set of tasks where some tasks have to run before other specific tasks.

The `MDAnalysis` guides have good examples for using `joblib`  to parallelize analysis code: [https://userguide.mdanalysis.org/stable/examples/analysis/custom\_parallel\_analysis.html](https://userguide.mdanalysis.org/stable/examples/analysis/custom_parallel_analysis.html).

asyncio
-------

asyncio is useful for scheduling and coordinating other tasks that are running at the same time. **asyncio runs on a single CPU**, so if you are limited by how fast Python runs, it won't save you.

For example, asyncio is useful for managing multiple GROMACS simulations in a sampling algorithm, like our own NEUS and STePS.

Dask
----

Dask is a very full featured solution to many parallelization and concurrency problems. Its documentation is unfortunately very variable in quality, and sometimes blatantly wrong. There are also occasional bugs in the code, so be wary.

GPU Programming
===============

Jax
---
Jax support drop-in acceleration with GPUs for matrix-multiply heavy code!
Having issues with multiple GPUs? Try [setting the appropriate environment variables](./multiple-notebooks-jax.md).

CuPy
----

CuPy is almost a drop-in replacement for NumPy that runs on GPUs.

Numba
-----

Numba can also make code run on GPUs. Like with CPUs, it is useful for numerical, loop-heavy code. However, due to the nature of GPUs, this code should be run on many elements for there to be a speed up.

PyTorch
-------

PyTorch (and other neural network libraries, like TensorFlow) runs on both CPUs and GPUs. Unlike CuPy, PyTorch is subtly different from NumPy.

RAPIDS
------

Implements many pandas and scikit-learn algorithms for GPU. This is a very new project, so the code isn't very well tested. Also, things tend to break pretty often.
