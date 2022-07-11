Problem
-------

After installing Anaconda on Midway, ThinLinc doesn't connect after logging in.

Solution
--------

This issue results from Anaconda's Python replacing the default Python, which ThinLinc uses to log in. This can be solved by not activating Anaconda or by intelligently deciding whether to load Anaconda.

Solution:

1.  Log in to Midway using ssh
2.  Run `conda config --set auto_activate_base false`