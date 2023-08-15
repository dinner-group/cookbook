# Alpha-helical-content-of-protein-sequences.md
Secondary structure motifs like  $\alpha $-helices or $\beta$-sheets are key for protein function. Therefore, reliable and consistent ways to quantify them can become pretty handy to study a given structure (or set of structures). It can also be very useful if you want to bias against the formation/melting of such structures in the context of Umbrella Sampling, for example, in order to find relevant CVs that can do that.

In the case of  $\alpha $-helices, which is what we'll talk about here, it is not obvious however how this quantification should be done. How do you determine how "helical" an amino acid sequence is? One way to do it is to measure to what extent the sequence deviates from a reference structure, computing some form of RMSD (e.g. between $\alpha$-carbons). This reference structure can be the same protein's folded helix (if such structure is available). If I am not mistaken, this is what people in the group did in the Trp-cage paper.

Alternatively, you can use an idealized helix model. This is what Plumed does with the function [ALPHARMSD](https://www.plumed.org/doc-v2.5/user-doc/html/_a_l_p_h_a_r_m_s_d.html), which is relatively straightforward to use. In its simplest version, you just need to specify the residues you want to include, i.e. the ones that should be forming or not the helix. From there, it will compute the normalized RMSD (from 0 to 1) of any chain of six contiguous residues, adding them up at the end. Thus, since for a 10-residue sequence, for example, for which you can make 5 different contiguous segments of 5 residues, the ALPHARMSD can go from 0 (totally melted) to 5 (totally folded). You can check the website for more details.

$$ \alpha = \sum_i 1−(r_i−d_0R_0)n_1−(r_i-d_0R_0)m
\\begin{array}{l}\\displaystyle \\alpha = \\sum\_i \\frac{ 1 - \\left(\\frac{r\_i-d\_0}{R\_0}\\right)^n } { 1 - \\left(\\frac{r\_i-d\_0}{R\_0}\\right)^m }\\end{array} 
$$

The function does contain some parameters to play with if you want though. In this post, I'd like to give a little bit of intuition about how being careful with these can help you to have more control when biasing against the melting/folding of a helix. Specifically, we will focus on how the choice of $R_0$ can change things. You can already imagine that a larger $R_0$ will make the measure a bit more relaxed, so larger deviations from the reference $d_0$ will be tolerated. The default value of $R_0$ is 0.08 nm, which is quite restrictive in my experience. We are going to try both 0.1 and 0.17 nm.

We are going to look at the insulin's A1 helix (I think this name was invented by Andrei Tokmakoff, but we are going to use it), located in the N-terminus of the A-chain (from A1 to A9, circled in pink). We will call the alpha content $\alpha$−A1A9. Since it has 9 residues, $\alpha$-A1A9 an go from 0 (totally melted) to 4 (totally folded):



![](/download/attachments/269226145/Fig1.png?version=3&modificationDate=1616195208000&api=v2)



Here's how the alpha content of the A1 helix in a 2000 steps trajectory evolves (ignore the time units). 

![](/download/attachments/269226145/Wiki_trajout_16.png?version=1&modificationDate=1616191244000&api=v2)

Without looking at any structures, we can expect the helix to be quite folded for the first 1000 steps, as both $\alpha$−A1A9 and $\alpha$−A1A9 $R_0= 0.17$ remain fairly close to 4. As expected, $\alpha$−A1A9$ $R_0=0.10$ is a bit lower as it is a bit more restrictive. Hoverer, after 1500 steps we observe that $\alpha$−A1A9$ $R_0 = 0.10$ is reduced to more than half its value, for which (if we didn't know about $\alpha$−A1A9$ $R_0 = 0.17$) we could expect a relatively melted helix. However, when we look at the structures at those times:



![](/download/attachments/269226145/Fig3.png?version=1&modificationDate=1616192762000&api=v2)

We observe that the helix isn't really melted. If anything, the inner grooves have increased a bit in diameter. Since in this configuration atoms depart from the reference helix structure Plumed has, $\alpha$−A1A9$ $R_0 = 0.10$ is lowered, but not in a physically meaningful manner. This is a problem with this function: when biasing against it to induce the melting of the helix, if we use a too strict ARMSD, many times it just increases the size of the grooves instead of really melting the helix. In that sense, we see how using $\alpha$−A1A9$ $R_0 = 0.17$  seems a bit more robust, as it does not decrease much at $t=1500$ but considers the helix to be mostly folded. In that sense, if we were biasing against it, plumed could not limit itself to simply widening the grooves, but should instead try something more "aggressive" like really melting the helix by stretching it (which is likely closer to what we want). 

Now we are going to look at 2 different trajectories (Traj 1 and Traj 2), projected on the $\alpha$−A1A9$ $R_0 = 0.10$ space:

![](/download/attachments/269226145/Fig4.png?version=1&modificationDate=1616193487000&api=v2)Without looking at the structures, we could predict that both trajectories present fairly melted helices (particularly Traj 1), and a subtle folding as in Traj 2 as time increases. However, if we look at some structures along both trajectories:

![](/download/attachments/269226145/Fig6.png?version=3&modificationDate=1616194151000&api=v2)

We see that structures are quite different! While the helix in Traj 1 is pretty much melted all the time (which is actually well predicted by $\alpha$−A1A9$ $R_0 = 0.10$), the helix in Traj 2 is actually not so melted (particularly as time progresses). In fact, a helical structure can be clearly devised, even though it is not perfectly folded. However, when using $R_0 = 0.10$, it seems like there's very little difference between one trajectory and the other. $\alpha$−A1A9$ $R_0 = 0.10$ is so restrictive that it just considers both trajectories totally or very close to totally melted, thus being very insensitive to differences between them. This is interesting, because in the previous example it was rather hypersensitive!

If we now project the same 2 trajectories on $\alpha$−A1A9$ $R_0 = 0.17$:

![](/download/attachments/269226145/Fig8.png?version=2&modificationDate=1616194189000&api=v2)





We see how using $R_0 = 0.17$ we are able to distinguish both trajectories better, and places Traj 2 around 2 (i.e. not folded but not totally melted). Note that Traj 1 does not reach 0 in this case, likely because some sort of loop remains in the furthest part of the sequence.



All things considered, you can see how using a a larger $R_0$ allows us to gain sensibility in the lower part of the coordinate, but to pay less attention to changes in the structure in more folded sequences (like a widening in a groove). This turns out to work better to bias towards melting, as unfolding typically proceeds through the stretching of the helix (as opposed to widening the groves). It is also better when biasing towards folding, as the coordinate is more capable of distinguishing the increasing formation of helical subunits that end up inducing the folding. As you can imagine, if you pick a too loose $R_0$, your coordinate might be too insensitive overall, considering really unfolded structures as folded. You have to play around to see what works best for your system. I haven't tried, but playing with other parameters in the function might help you in that sense!

Something that has worked really well for me is linearly combining $\alpha$−A1A9$ with some other measure of unfolding like the distance between the two extrema of the helix (which typically increases when the helix melts and the sequence stretches). This way plumed avoids trying to widen the grooves and you usually obtain more control over the process.
