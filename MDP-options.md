# MDP options
[Here](http://manual.gromacs.org/documentation/2019.4/user-guide/mdp-options.html) are the options available. You should have already looked through the Lysozyme in Water tutorial, which introduces many of the mdp options you need to know. Here, we will discuss some of the defaults in the Dinner Group (specifically those that are different than what is seen in the Lysozyme in Water tutorial and/or CHARMM\_GUI defaults), and why we generally think them to be best practices. 
These are also applicable to other simulation engines, but you will have to dig through the documentation to find the appropriate flags.

*   `integrator = sd `← This option sets the simulation be be [Langevin Dynamics](http://manual.gromacs.org/documentation/2019.4/reference-manual/algorithms/stochastic-dynamics.html), which is our preferred integrator for NVT simulations. This integrator is fairly accurate, as deemed by Charlie Matthews, who spent his PhD trying to find the best [Langevin Dynamics integrator](https://academic.oup.com/amrx/article/2013/1/34/166771). Generally, we prefer NVT simulations over NPT simulations, as most of the barostats in GROMACS are relatively poorly-behaved (at least when compared to the Langevin thermostat). In particular, Parrinello-Rahman barostat (and the Nose-Hoover thermostat, for that matter) decay in an oscillatory manner to the target pressure/temperature. These oscillations are aphysical, and can lead to unexpected behavior (and thus pathological results). I **highly** recommend you read through the GROMACS manual entry on [Molecular Dynamics](http://manual.gromacs.org/documentation/2019.4/reference-manual/algorithms/molecular-dynamics.html) to explicitly compare existing options. 
*   `ref_t = 303.15 `← Reference temperature in K. It is best to use something in the range of 300 K - 303.15 K
*   `tau_t = 2 `← The time constant (in ps) for the friction applied by the sd integrator. The friction constant (in ps\-1) is 1/τ. As noted in the GROMACS manual, the default for the friction constant is 0.5 ps\-1, meaning you set the time constant τ=2 ps. You should apply this friction to all atoms in your system (both PROT and SOL\_ION, if you are using CHARMM\_GUI). However, keep in mind that this friction biases dynamics of your system. If you are working on non-dynamical simulation (like Umbrella Sampling, for example), this is fine. However, if you care about the dynamics (for building a MSM or running DGA, for example), then you want this friction to be as weak as possible, while still thermostating the system effectively. You can play around to find where this point is, but setting τ=10 ps has worked for me. 
*   `DispCorr = no `← For CHARMM force fields, generally we do not want to apply the Dispersion Correction.
*   `constraint_algorithm = LINCS `← Our preferred constraint algorithm to ensure bond distances do not change when we don't want them to. 
*   `comm_mode = linear`   ← Remove center of mass translational velocity, so ideally your system doesn't float and cross the boundary. Although this can sometimes (most times) not work completely. 
*   From the [User Guide](http://manual.gromacs.org/documentation/2019.4/user-guide/force-fields.html#charmm) (which, again, I **highly** recommend you read through), the following are the settings that should be used for CHARMM Force Fields (our current most preferred force field is [CHARMM36m](https://www.nature.com/articles/nmeth.4067), as discussed in [Building a System With CHARMM-GUI](./Building-a-System-With-CHARMM-GUI.md) 


    constraints = h-bonds
    cutoff-scheme = Verlet
    vdwtype = cutoff
    vdw-modifier = force-switch
    rlist = 1.2
    rvdw = 1.2
    rvdw-switch = 1.0
    coulombtype = PME
    rcoulomb = 1.2
    DispCorr = no

Also, for energy minimization, and the initial steps of both NVT and NPT equilibration, you will need position restraints turned on, so you can equilibrate the system around the protein without significantly varying the protein's coordinates. You can do this by defining something like the following in your .mdp file (example uses the CHARMM-GUI conventions)

*   `define = -DREST_ON -DSTEP4_1`
*   `refcoord_scaling = com`

As far as output, GROMACS generates a whole cadre of files by default. Normally, we won't need the vast majority of these files (perhaps excluding the initial equilibration), and will instead use a wrapper like PLUMED to output any collective variables of interest. Specifically, we don't need the .`trr` trajectory files (normally), as these take up a large amount of storage space. The following commands will suppress most default output, and only let you output the compressed `.xtc` files - you can reanalyze these trajectories (and for example, output new collective variables, or system variables like temperature or energy) with either GROMACS or PLUMED after generation, if you so desire. 

    nstlog = 0
    nstxout = 0
    nstvout = 0
    nstfout = 0
    nstcalcenergy = 0
    nstenergy = 0
    compressed-x-grps = PROT SOL_ION
    nstxout-compressed = 5000

Keep in mind that if you are using groups (`compressed-x-grps`) in your `.mdp` file, you need to specify the identity of these groups in your .ndx file. You can either do this manually, or automatically do so using CHARMM\_GUI. If you choose to do so manually,  you can use something like VMD to load the structure, select certain atoms using the TCL console, and print out their atom indices. Alternatively, you could use bash to `grep` through a structure file to get the appropriate atom indices. 

**Overall, your mdp settings are extremely important.** The accuracy of any potential project is entirely predicated on using appropriate settings in your MD engine. As such, **make sure to go through every line in your mdp file before starting large simulations.** You should understand what each flag is doing, and why you have included it. You should go through the available [documentation](http://manual.gromacs.org/documentation/2019.4/user-guide/mdp-options.html) and make sure there isn't something else you should be setting. For the first few times, it's also probably a good idea to ask someone else to look through your mdp file just to make sure everything is good. The absolute last thing you want is to spend 500k SUs on a large simulation, then be forced to redo it because some seemingly-minor mdp flag was set incorrectly.