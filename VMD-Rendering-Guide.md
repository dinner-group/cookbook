This guide was originally developed by Lu Hong, and has since been (lightly) expanded by Adam Antoszewski. The normal VMD defaults are not suited for publication-quality figures.

**[HERE](/download/attachments/232101322/VMDRC?version=1&modificationDate=1591802932000&api=v2)** is a sample .vmdrc file that will set most of the defaults listed below. You can save this as `${HOME}/.vmdrc` and these settings will apply by default to VMD. 

General settings
----------------

1.  White background: Graphics → Colors → Display → Background → 8 White
2.  Orthographic projection (to please Aaron): Display → Orthographic
3.  Turn off axes: Display → Axes → off
4.  Only show solvent atoms when relevant. However, remember that they are still there, and play a vital role in most protein-related processes.
5.  Ray tracing options: Display → Display settings
    1.  Set Shadows and Amb. Occl. both to On
    2.  In general, AODirect × num.Lights + AOAmbient ≈ 1.8; I usually use AO Ambient = 0.80 and AO Direct = 0.40.
6.  You can select specific atoms to visualize through typing atom selection command in the _Selected Atoms_ box of the Graphics → Representations menu. Some useful keywords:
    1.  protein - only select atoms belonging to the protein
    2.  water/ion/solvent- only select water, ions, or all solvent atoms. 
    3.  backbone - only protein backbone atoms
    4.  noh - all protein heavy atoms (anything in the protein but hydrogens)
    5.  sidechain - only protein sidechain atoms
    6.  resid - specific residue id numbers, indexed from 1
    7.  index - atom ID, **indexed from 0**. Note that this does not match with the PDB atom ID, as those are indexed from 1. This is the convention, though, for things like PyEMMA.
    8.  serial - atom ID, **indexed from 1**. These will match the PDB IDs, and can referenced in GROMACS .ndx files
    9.  chain/fragment - Specific fragments of a protein/complex, if there are multiple non-connected units. 
    10.  Many other options are listed under Graphics → Representations → Selections
7.  Tachyon options: File → Render…
    1.  Render the current scene using → Tachyon
    2.  Optional render command:
        1.  \-res x y: set the resolution of rendered image to x by y. I usually use 2000 by 2000 or higher for publications and 500 by 500 when testing.
        2.  \-trans\_max\_surfaces 1: make transparent surfaces easier to see through by restricting the number of shown transparent surfaces to 1. Only affect materials that have transparency.
        3.  \-shadow\_filter\_off: materials with transparency cast no shadow.

Tips for close-ups
------------------

1.  Turn off depth cuing: Display → Depth Cuing
2.  It is useful to re-center the view by pressing “C” followed by an atom selection on screen.
3.  For showing chemical structures:
    1.  For drawing method, Licorice is good for showing chemical structure, while VDW is good for showing sterics and/or contacts.
    2.  For material, use either Diffuse (preferred), AOShiny, AOChalky or AOEdgy. Alternatively, use Goodsell material for a pencil drawing style. The default coloring method is often sufficient.
    3.  Set Bond Radius to 0.2 for slightly less cluttering if using Licorice.
    4.  Use the atom selection command “and not (hydrogen and within 1.5 of carbon)” to show hydrogen atoms attached to heteroatoms only.
    5.  For hydrogen bonds (draw method HBonds), set Line Thickness to 3.
    6.  If you want to show water structure with Licorice, do not load your structure with a topology file. 
        1.  To keep waters whole, use the "same residue as" atom selection command. For example, to show waters within 3 angstroms of the heavy atoms of the sidechain from residue 10, one can type "same residue as (water within 3 of (sidechain and resid 10))"
4.  For showing protein secondary structure:
    1.  If the secondary structures obscure important residue structures, use NewCartoon with either Ghost (preferred) or Transparent material with the -trans\_max-surfaces 1 and -shadow\_filter\_off options. Otherwise see the next section.
    2.  Use Silver for Ghost material or White for Transparent material.
    3.  You can adjust the opacity of the Ghost material, or any other material parameter, through the Graphics → Materials menu. Note that the opacity will vary dramatically between the VMD window and Tachyon render. 

Tips for wide shots
-------------------

1.  For drawing method, NewCartoon is good for showing secondary structures, while Surf is good for showing sterics and/or contacts. For material, use either Diffuse (preferred), AOShiny, AOChalky or AOEdgy.
2.  To make surface representations smoother, do not include hydrogen atoms in atom selection.
3.  To show a Surf representation on top of NewCartoon, set the Surf material to Glass1 and color to White. Alternatively, use Ghost in conjunction with the -shadow\_filter\_off option.
4.  A nice coloring method (esp. for multimeric proteins) for NewCartoon is coloring by Index, which gives a color gradient over the atom indices. One can control the atom range over which the color gradient is computed at Trajectory → Color Scale Data Range.

Tips for trajectories
---------------------

1.  When loading trajectories (especially large ones), it is **much** faster to either load via the command line (i.e., `vmd struct.gro traj.xtc` on the command line), or by checking the 'Load all at once' radio button under File → New Molecule.
2.  For viewing trajectories, it is often best to align the protein backbone/ atom selections, to remove any center of mass motion of rotation. You can do this by going to Extensions → Analysis → RMSD Trajectory Tool → Align. The default atoms to align against are the protein heavy atoms, although you can change this. 
3.  If your selection changes between frames of a trajectory (i.e., selecting waters within a cutoff distance, or hydrogen bonds), you will need to select the _Update Selection Every Frame_ option from the Graphics → Representations → Trajectory menu.
4.  To show disorder of a certain section from a trajectory in just one frame, you can make an appropriate atom selection and use the _Draw Multiple Frames_ option from the Graphics → Representations → Trajectory menu.
5.  You can smooth your trajectories for easier visualization by using the _Trajectory Smoothing Window Size _slider. This can sometimes distort the trajectory, however, so use with care.

Misc. comments
--------------

In general, do not show multiple identical representations of the same structure with different colors, because the way Tachyon resolves z-fighting is different from that in the Snapshot (i.e., what is shown in the main display window). If you want to highlight a segment of a structure with different colors, do so with two non-overlapping representations.

The Tachyon engine does not support GPU acceleration (yet), so the best option for rapid image rendering is logging onto Midway with ThinLinc (or other connection methods that support X forwarding) and requesting an interactive job with a node.

One can save almost all settings used in rendering an image with File → Save Visualization State…, which generates a script that can be read using the tag “-e scene\_file.vmd”. However, the script does not save the axes settings or the Tachyon settings. This is **super** useful to save time. However, loading these visualization states, for reasons that are beyond me, can be little testy. Sometimes, if you try to load via the -e flag, or the File → Load Visualization State tab, you will get a segmentation fault. If this happens, try calling vmd (without loading anything), then type some garbage command (sdhfbsi will work, anything it doesn't recognize). Then, load the visualization state by typing `source VMD_FILE.vmd` into the command line. Most of the time, that will work. Again, why this works is beyond me. 

Every setting discussed so far can also be done with a command in a script file. TCL scripting is discussed more in [VMD as an Analysis Tool](/display/thecookbook/VMD+as+an+Analysis+Tool). This can be useful for rendering a lot of images in a similar way (e.g., for a movie), or for using VMD as a tool to actually analyze your simulations, instead of just visualizing them. 

It is always a good idea to use Photoshop (or similar software) to do some post-processing (cropping white space, adjusting white balance, etc.)

The default labelling tools for atoms, bonds, angles, etc (found under Mouse → Label) are likely not suitable for publication. If needed, you should add these labels in with some post-processing software. 

Again, **[HERE](/download/attachments/232101322/VMDRC?version=1&modificationDate=1591802932000&api=v2)** is a sample .vmdrc file that will set most of the defaults listed above. Just in case you missed it before.