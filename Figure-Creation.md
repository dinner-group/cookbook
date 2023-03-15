# Figure Creation
Everyone needs to make figures, and sometimes that process can be a little...complicated. If you are looking for a guide on how to render high-quality molecular images from VMD, check out the [VMD Rendering Guide](./VMD-Rendering-Guide.md). This section, instead, will focus on various tips and tricks for commonly used figure generation/post-processing tools, from Python to Inkscape. Feel free to add any time you find something useful! 

Making nice plots in Matplotlib
===============================

The defaults in the Matplotlib package pretty ugly, so it's worth spending some time playing around with the settings to change the defaults.
The primary method of changing settings is using the [`` `rc` `` file](https://matplotlib.org/3.5.0/tutorials/introductory/customizing.html), which allows you to either fix the settings for a given figure using a Python context manager (i.e. the `with plt.rc[...]` syntax), or by changing the so-called "stylesheet." These files are typically found in your directory `~/.matplotlib/stylelib/` or `~/.config/matplotlib/stylelib/` and allow you to override the default matplotlib settings. In particular, you can define a custom style sheet with your desired settings and just turn it on whenever you use matplotlib, without having to think too much. An example file called `custom.mplstyle` is [here](./files/custom.mplstyle), and to activate it you would simply add it to the previously-mentioned directory and then call `plt.style.use("custom")` in your Python script/Jupyter notebook.

I've also found the following [cheatsheets](https://github.com/matplotlib/cheatsheets) from the developers of Matplotlib to be extremely helpful. (I keep a copy on my desktop at all times to refere to.)

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


# Rendering publication-quality images
Typically speaking, you will want to avoid image formats such as `.png` or `.jpg` given that these are compressed (many journals also do not accept `png` files).
Instead, your figures should ideally be in *vector graphics* format, which basically means that they can be resized indefinitely without losing quality (this is because vector graphics formats basically encode the geometrical information needed to scale an image at any size).
Examples of vector graphics formats include `.svg`, `.pdf` (try zooming in one one of your PDF texts once and see that the edges of the letters don't degrade in sharpness), and `.eps`. 
My preferred format is `.pdf` since it integrates very smoothly with LaTeX and can be opened in basically any software.

In particular, when you go to save an image in Matplotlib, use the following lines to get your plot/image in the `pdf` format:
```
# make image 
fig = plt.figure(figsize=(width, height))
img = plt........
plt.savefig("NAME.pdf", bbox_inches='tight')
```
The keyword argument `bbox_inches='tight'` insures that the edges of your figure don't get cut off.
Note that you can set the exact size of your image in the `figsize` keyword argument (which is by default in units of **inches**) for proper sizing.

(As a rule of thumb, two column-wide figures should be around 6.5 inches width and one-column wide figures should be around 3.25 inches wide. Check the journal you're submitting to for more detailed information.)

Finally, it's important to note that for image-like plots with lots of info such as `pcolormesh` or `scatter`, the default saving as `pdf` format will make every single square or point a different vector graphic and probably make your image impossibly slow to load.
To get around this, you should set the `rasterized=True` keyword in making your plot.
Matplotlib has a good [example](https://matplotlib.org/stable/gallery/misc/rasterization_demo.html) of how to do this.
Note that the rasterization requires a `dpi` specification to determine the quality level, since it no longer has the same scaling properties as a vector graphic.
In general, **500 dpi** is usually a good setting for publication-quality figures.

```
# example:
fig = plt.figure()
img = plt.scatter(x, y, rasterized=True)

# set dpi for rasterized part (i.e. the scatter plot)
plt.savefig("NAME.pdf", dpi=500, bbox_inches='tight')
```
