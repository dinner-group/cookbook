# Figure-Creation.md
Everyone needs to make figures, and sometimes that process can be a little...complicated. If you are looking for a guide on how to render high-quality molecular images from VMD, check out the [VMD Rendering Guide](/display/thecookbook/VMD+Rendering+Guide). This section, instead, will focus on various tips and tricks for commonly used figure generation/post-processing tools, from Python to Inkscape. Feel free to add any time you find something useful! 

Making nice plots in Matplotlib
===============================

The defaults in the Matplotlib package pretty ugly, so it's worth spending some time playing around with the settings to change the defaults. The primary method of changing settings is using the [`` `rc` `` file](https://matplotlib.org/3.5.0/tutorials/introductory/customizing.html), which allows you to either fix the settings for a given figure using a Python context manager (i.e. the `with plt.rc[...]` syntax), or by changing the so-called "stylesheet." These files are typically found in your directory `~/.matplotlib/stylelib/` or `~/.config/matplotlib/stylelib/` and allow you to override the default matplotlib settings. In particular, you can define a custom style sheet with your desired settings and just turn it on whenever you use matplotlib, without having to think too much. An example file called `custom.mplstyle` is [here](/download/attachments/265716067/custom.mplstyle?version=1&modificationDate=1653859854000&api=v2), and to activate it you would simply add it to the previously-mentioned directory and then call `plt.style.use("custom")` in your Python script/Jupyter notebook.

Useful packages
---------------

### Seaborn

A [Python plotting package](https://seaborn.pydata.org/index.html) which extends a lot of Matplotlib's functionality, while enabling more complex control and generally better-looking aesthetics. Their [colormaps](https://seaborn.pydata.org/tutorial/color_palettes.html) are quite nice and they have good [default style settings](https://seaborn.pydata.org/tutorial/aesthetics.html) if you don't want to spend a bunch of time designing your own.

### Prettypyplot

[Makes](https://gitlab.com/braniii/prettypyplot) your scatter plots, colorbars, legends, etc. all look nicer.

### SciencePlots

[Python package](https://github.com/garrettj403/SciencePlots) which has good default styles which make your plots look like they came from Nature or Science. Also includes several color cycles from Paul Tol.

Color schemes and colormaps
===========================

The default matplotlib colormap (viridis) is not bad, but you can also define your own. I personally very much enjoy the ones from [Paul Tol](https://personal.sron.nl/~pault/), as well as the `seaborn` ones, though defining your own can be quite annoying to do in matplotlib. Here's an example for a diverging colormap (e.g. for plotting committors):
    
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    # from Paul Tol's website
    colors = mpl.colors.to_rgba_array(
    [
    "#364B9A",
    "#4A7BB7",
    "#6EA6CD",
    "#98CAE1",
    "#C2E4EF",
    "#EAECCC",
    "#FEDA8B",
    "#FDB366",
    "#F67E4B",
    "#DD3D2D",
    "#A50026",
    ]
    )
    
    cm_div = mpl.colors.LinearSegmentedColormap.from_list("diverging", colors)
    # this allows you to refer to the colormap by its name ("diverging" in this case)
    mpl.colormaps.register(cm_div, force=True)  
    
    # plot something
    x = ...
    y = ...
    z = ...
    
    plt.pcolor(x, y, z, cmap='diverging')

[![](/s/-tpdgys/8803/fjj6gm/5.1.2/_/download/resources/com.atlassian.confluence.plugins.confluence-view-file-macro:view-file-macro-resources/images/placeholder-medium-file.png)custom.mplstyle](/download/attachments/265716067/custom.mplstyle?version=1&modificationDate=1653859854000&api=v2)