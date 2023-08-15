# I can't run multiple Jupyter notebooks with GPUs in Jax


If you try requesting multiple GPUs and running a Jupyter notebook with Jax thinking that you can have one GPU per notebook, you'll discover that this doesn't work. You'll get some weird error about dispatching code and CUDA complaining.

## Solution
Use the `CUDA_VISIBLE_DEVICES` environment variable to choose which of the GPUs you want to use for that notebook.

Say you have requested 2 GPUs. The node will label them starting from 0, so they will be identified as `gpu:0` and `gpu:1` if you call `jax.devices()`. 
Now, before you load Jax run
```
import os
os.environ['CUDA_VISIBLE_DEVICES'] = 'XX'
import jax
print(jax.devices())
```
where `XX` is the number of the GPU you want to use for that Jupyter kernel (if you have 2 GPUs, then set `XX` to 0 for one notebook and 1 for the other).
This should yield the output something like `[StreamExecutorGpuDevice(id=0, process_index=0)]` corresponding to the GPU you chose. You can then run calculations normally.