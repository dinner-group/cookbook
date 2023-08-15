# Run-Jupyter-Notebooks-on-a-Compute-Node.md
Jupyter notebooks are convenient for plotting and exploratory coding but running them on your computer or on a login node is often not such a great idea when you're doing something computationally intensive, such as training a neural network. Running them on compute nodes will give you (and everyone else) a much better time. Note that compute nodes don't have internet access.

Step-by-step guide
------------------

1.  Create a sbatch script to run a Jupyter notebook. The `jupyter` command needs the flags `--no-browser --ip=$(hostname -i)` passed to it. For example,
    
```
#!/bin/bash
 
#SBATCH --job-name=jupyter
#SBATCH --output=jupyter.out
#SBATCH --error=jupyter.err
#SBATCH --partition=weare-dinner2
#SBATCH --account=weare-dinner
#SBATCH --qos=weare-dinner
#SBATCH --time=6:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=28
#SBATCH --mem=57G
 
# load Anaconda here
 
jupyter notebook --no-browser --ip=$(hostname -i)
```
    
2.  Submit the sbatch script. The error file, in the case of the above script `jupyter.err`, will contain something along the lines of
   
```
To access the notebook, open this file in a browser:
    file:///home/chatipat/.local/share/jupyter/runtime/nbserver-15916-open.html
Or copy and paste one of these URLs:
    http://10.50.222.219:8888/?token=b3bd170eb05300fa7cb3b4ece15efd2980cf1ec2e3b58802
 or http://127.0.0.1:8888/?token=b3bd170eb05300fa7cb3b4ece15efd2980cf1ec2e3b58802
```
    
If you are on the campus internet or are using ThinLinc, you can connect to the Jupyter notebook with the URL that's not 127.0.0.1. In the case above, http://10.50.222.219:8888/?token=b3bd170eb05300fa7cb3b4ece15efd2980cf1ec2e3b58802 will connect you to the Jupyter notebook.  
    
Otherwise, you'll need to make an ssh tunnel into the compute node. For the case above, running on your computer `ssh [username@midway2.rcc.uchicago.edu](mailto:username@midway2.rcc.uchicago.edu) -L 9000:10.50.222.219:8888` (9000 here is an arbitrary number; using anything in the range 8888–9999 should be safe) will allow you to connect to the Jupyter notebook using the URL http://127.0.0.1:9000/?token=b3bd170eb05300fa7cb3b4ece15efd2980cf1ec2e3b58802. Adding the `--port` option prevents from the a port-conflict issue. For example:

```
jupyter notebook --no-browser --ip=$(hostname -i) --port=any_number_between_15000_30000 
```
    