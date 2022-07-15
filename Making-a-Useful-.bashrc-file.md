# Making a Useful .bashrc file
`.bashrc` files are particularly useful for automating common commands you run on the bash terminal. You should be very liberal in defining aliases that maximize efficiency. I find the most helpful ones are squeue commands that check jobs currently running, or sinteractive commands to start interactive sessions. In general, we have found that you should not load any modules in your bashrc, particularly anaconda. I alias short commands to load specific modules, instead. Below is my .bashrc file - note in particular the squeue commands that specify exactly the information I want to see, including the number of cores requested for each job. 

```
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi
# User specific aliases and functions
alias clr="clear"
alias ll="ls -alh"
alias ml="module load"
alias rm="rm -i"
alias size="du -sh"
alias ldir="ls -al | grep ^d"
alias home="cd ~"
alias scratch="cd /scratch/midway3/scguo"
alias proj="cd /project/dinner/scguo"
alias bdinner="cd /beagle3/dinner/scguo"
alias ..="cd ../"
alias ...="cd ../../"
alias ....="cd ../../../"
alias .....="cd ../../../../"
alias mv="mv -i"
alias cp="cp -i"
alias attach="tmux attach -t"
alias tls="tmux ls"
alias tmux="tmux -2"
alias rename="tmux rename-session -t"

# Slurm aliases
# alias gmx="gmx_mpi"
alias sb="sbatch"
alias sc="scancel"
alias jobs="squeue -u scguo -o \"%.18i %.16P %.16j %.8u %.2t %.10M %.10L %.6D %.6C %.10m %.6p %R \""
alias sqd="squeue -p 'dinner,dinner-hm' -o \"%.18i %.16P %.16j %.8u %.2t %.10M %.10L %.6D %.6C %.10m %.6p %R \""
alias sqb="squeue -p beagle3 -o \"%.18i %.16P %.16j %.8u %.2t %.10M %.10L %.6D %.6C %.10m %.6p %R \""
alias mlv="module load vmd/1.9.3"
alias mlp="module load python/3.7.0"
alias sid="sinfo -p dinner"
alias sib="sinfo -p beagle3 -O 'partition,available,nodes,features,statecompact,nodelist'"
alias sintd="sinteractive -p dinner --account=pi-dinner --qos=dinner --nodes=1 --ntasks=1"
alias sintd8="sinteractive -p dinner --account=pi-dinner --qos=dinner --nodes=1 --ntasks=1 --cpus-per-task=8"
alias sintd48="sinteractive -p dinner --account=pi-dinner --qos=dinner --nodes=1 --ntasks=1 --cpus-per-task=48"
```
