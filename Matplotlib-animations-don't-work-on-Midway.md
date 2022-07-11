# Matplotlib-animations-don't-work-on-Midway.md
Problem
-------

Animations made with matplotlib.animation don't display or save; instead giving a very long incomprehensible stream of errors. Examples from Matplotlib's website don't work. This occurs in both scripts and notebooks.

Solution
--------

The issue results from Anaconda's (or pip's) version of FFmpeg (which is used to make the animation) not supporting the video format (due to patent licensing issues). This can be solved by using the FFmpeg program installed on Midway.

Tell Matplotlib to use Midway's version of FFmpeg:  

1.  Load the FFmpeg module:  
    `module load ffmpeg` 
2.  Find where FFmpeg is located:  
    `which ffmpeg`  
    This will give an output like  
    `/software/ffmpeg-3.2-el7-x86_64/bin/ffmpeg` 
3.  Add the path to the `.matplotlibrc` file (you may need to create it). For example, with the output above, add  
    `animation.ffmpeg_path: /software/ffmpeg-3.2-el7-x86_64/bin/ffmpeg`
    
4.  Load the FFmpeg module before launching Python

Instead of modifying `.matplotlibrc` , `animation.ffmpeg_path`  may also be set in the Python script (order is important!)

    import matplotlib.pyplot as plt
    plt.rcParams['animation.ffmpeg_path'] = '/software/ffmpeg-3.2-el7-x86_64/bin/ffmpeg' 
    import matplotlib.animation as animation

An alternative (partial) solution that doesn't involve Midway's FFmpeg package is to install FFmpeg from conda-forge:

`conda install -c conda-forge ffmpeg` 
