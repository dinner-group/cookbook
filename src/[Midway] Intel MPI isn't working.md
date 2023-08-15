# [Midway] Intel MPI isn't working

Problem
-------
Intel MPI throws an error like
```
Abort(1091215) on node 0 (rank 0 in comm 0): Fatal error in PMPI_Init_thread: Other MPI error, error stack:
MPIR_Init_thread(136).......:
MPID_Init(904)..............:
MPIDI_OFI_mpi_init_hook(986): OFI addrinfo() failed (ofi_init.c:986:MPIDI_OFI_mpi_init_hook:No data available)
```

Solution
--------
This problem occurs because Intel MPI is trying to use the fast InfiniBand connection between nodes (this happens even when you're using only a single node) but something isn't configured correctly. A workaround is to add
```
export FI_PROVIDER=tcp
```
after MPI is loaded but before it is first used (i.e., after all the `module load` statements but before everything else). This tells Intel MPI to use the slower ethernet connection between nodes. Note that if you need fast communication between nodes (e.g., when running a single molecular dynamics simulation on multiple nodes), this is probably too slow, and you'll need to find a better solution (e.g., figure out which nodes have working InfiniBand).
