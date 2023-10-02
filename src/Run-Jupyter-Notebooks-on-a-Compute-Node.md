# Run-Jupyter-Notebooks-on-a-Compute-Node.md
Jupyter notebooks are convenient for plotting and exploratory coding but running them on your computer or on a login node is often not such a great idea when you're doing something computationally intensive, such as training a neural network. Running them on compute nodes will give you (and everyone else) a much better time. Note that compute nodes don't have internet access.

Step-by-step guide
------------------

1.  Create a sbatch script to run a Jupyter notebook. The `jupyter` command needs the flags `--no-browser --ip=$(hostname -i)` passed to it. For example,
    
```
#!/bin/bash
#
#BATCH --job-name=jupyter
#SBATCH --output=jupyter.out
#SBATCH --error=jupyter.err
#SBATCH --partition=dinner
#SBATCH --account=pi-dinner
#SBATCH --qos=dinner
#SBATCH --time=8:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=28
#SBATCH --mem=57G
 
# load Anaconda here

jupyter notebook --no-browser --ip=$(hostname -i)

```
    
2.  Submit the sbatch script. The error file, in the case of the above script `jupyter.err`, will contain something along the lines of
   
```
To access the notebook, open this file in a browser:
    file:///home/darrenjl/.local/share/jupyter/runtime/nbserver-605805-open.html
Or copy and paste one of these URLs:
    http://10.50.250.251:16000/?token=8b7d65e0ae44d21e3bc4ed9dcdc464196663b4fc48f2ef9d
or http://127.0.0.1:16000/?token=8b7d65e0ae44d21e3bc4ed9dcdc464196663b4fc48f2ef9d
```
    
If you are on the campus internet or are using ThinLinc, you can connect to the Jupyter notebook with the URL that's not 127.0.0.1. In the case above, copy-pasting http://10.50.250.251:16000/?token=8b7d65e0ae44d21e3bc4ed9dcdc464196663b4fc48f2ef9d into your browser will connect you to the Jupyter notebook.  
    
Otherwise, you'll need to make an ssh tunnel into the compute node. For the case above, running on your computer `ssh username@midway3.rcc.uchicago.edu -L 9000:10.50.222.219:8888` (9000 here is an arbitrary number; using anything in the range 8888–9999 should be safe) will allow you to connect to the Jupyter notebook using the 127.0.0.1 URL *except* where the last four numbers after 127.0.0.1 is replaced with your arbitrary number. After logging in, copy-pasting http://127.0.0.1:9000/?token=8b7d65e0ae44d21e3bc4ed9dcdc464196663b4fc48f2ef9d into your browser will open the notebook for the above example. Adding the `--port` option prevents from the a port-conflict issue. For example:

```
jupyter notebook --no-browser --ip=$(hostname -i) --port=any_number_between_15000_30000 
```