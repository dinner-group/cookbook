# Making-a-Useful-.bashrc-file.md
.bashrc files are particularly useful for automating common commands you run on the bash terminal. You should be very liberal in defining aliases that maximize efficiency. I find the most helpful ones are squeue commands that check jobs currently running, or sinteractive commands to start interactive sessions. In general, we have found that you should not load any modules in your bashrc, particularly anaconda. I alias short commands to load specific modules, instead. Below is my .bashrc file - note in particular the squeue commands that specify exactly the information I want to see, including the number of cores requested for each job. 

```
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific aliases and functions
alias anto="cd /project2/dinner/aanto"
alias siwd="sinteractive --account=weare-dinner --partition=weare-dinner2 --qos=weare-dinner -t 06:00:00"
alias siwd1="sinteractive --account=weare-dinner --partition=weare-dinner2 --qos=weare-dinner -t 12:00:00 --ntasks 12"
alias gmx="gmx_mpi"
alias sq="squeue --user=antoszewski -o \"%.18i %.16P %.16j %.8u %.2t %.10M %.6D %.6C %R \""
alias sqwd2="squeue -p weare-dinner2 -o \"%.18i %.16P %.16j %.8u %.2t %.10M %.6D %.6C %R \""
alias sqwd1="squeue -p weare-dinner1 -o \"%.18i %.16P %.16j %.8u %.2t %.10M %.6D %.6C %R \""
alias sqb="squeue -p broadwl -o \"%.18i %.16P %.16j %.8u %.2t %.10M %.6D %.6C %R \""
alias sqg="squeue -p gm4 -o \"%.18i %.16P %.16j %.8u %.2t %.10M %.6D %.6C %R \""
alias scr="cd /scratch/midway2/antoszewski"
alias sw="watch squeue --user=antoszewski"
alias pyt="export PATH=\"/project2/dinner/aanto/anaconda3/bin:$PATH\""
alias cds="cd /cds/weare-dinner/aanto"
alias mlv="module load vmd"
alias mlg="source /project2/dinner/gromacs/sourceme.sh"
```