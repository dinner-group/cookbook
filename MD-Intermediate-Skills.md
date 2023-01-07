# MD Intermediate Skills
Here will be a repository of informational pages meant for someone with an intermediate amount of experience using GROMACS and various analysis tools. These pages will cover more advanced sampling and analysis techniques, as well as interactions for installing various MD tools that a beginner user might not need. Before continuing to the pages herein, make sure you are familiar with all of the articles in [Molecular Dynamics Essentials](./Molecular-Dynamics-Essentials.md).

Useful packages
===============
These are packages which are generally essential in analyzing and computing relevant information from MD trajectories, especially if you don't want to wrangle PLUMED, or need something not implemented there.

* `pyemma`
    * Download [here](http://www.emma-project.org/latest/)
    * Tools for [featurizing](#featurization) MD trajectories, creating/analyzing MSMs, and plotting.
* `mdtraj`
    * Download [here](https://www.mdtraj.org/1.9.8.dev0/index.html)
    * Very _fast_ library for analyzing MD trajectories - note that it is optimized especially for RMSD calculations.
    * Also has a nice [selection syntax](https://www.mdtraj.org/1.9.8.dev0/atom_selection.html) like VMD which makes computing CVs easier
* `MDAnalysis`
    * Download [here](https://userguide.mdanalysis.org/stable/index.html)
    * _Extremely extensive_ library of analysis functions
    * In contrast to `mdtraj`, much slower for things like distance calculations. Part of the reason for this is that it doesn't load whole trajectories into memory. More flexible, however. 
    * Slightly [weird API](https://userguide.mdanalysis.org/stable/trajectories/trajectories.html) for dealing with trajectories

These three packages + your general Numpy/SciPy functions should be sufficient to compute almost anything you can imagine.


Featurization
=============
Often times, you need to be able to transform the raw coordinates of your protein ($\mathbb{R}^{3N}$) to something which is invariant to translations/rotations, and ignores the many solvent degrees of freedom.
There are many ways to do this, and we recommend checking out the plethora of [protein](https://doi.org/10.1021/acs.jctc.0c00933) [papers](https://www.nature.com/articles/nchem.2785) from [our group](https://doi.org/10.1021/acs.jpcb.1c06544) and [others](https://doi.org/10.1021/acs.jctc.6b00339).
These are typically easy to do in a package like `pyemma`. (See [above](#useful-packages).)