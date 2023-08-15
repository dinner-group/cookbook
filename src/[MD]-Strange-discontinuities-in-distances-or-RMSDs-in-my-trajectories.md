# [MD] Strange-discontinuities in distances or RMSDs in my trajectories
Problem
-------

After using PLUMED, I plot my distances (or RMSDs, or any collective variable calculated based on a distance) and see strange jumps/discontinuities. I know that these two atoms are not going from 5.0 nm apart to 0.3 nm apart within one frame. What's going on and how can I fix it?

Solution
--------

Short answer: [WHOLEMOLECULES](https://www.plumed.org/doc-v2.5/user-doc/html/_w_h_o_l_e_m_o_l_e_c_u_l_e_s.html) and NOPBC

Long answer: The default periodic boundary condition treatment in PLUMED is a little odd. So, for any distance it calculates, unless you tell it otherwise, it will immediately apply the minimum image convention.  In other words, using the below code, if the calculated distance is more than half the length of the box, it will automatically shift the position of the atoms (only for calculation purposes, not MD purposes) to make the distance as small as possible - this is, in theory, supposed to automatically account for molecules broken across periodic boundaries.

    #You know this distance should return 5.0 nm, but it instead returns 0.1 nm
    end_to_end_distance: DISTANCE ATOMS=1,201

Many times, however, this actually breaks the distance calculation, especially for large molecules. For example, imagine you have a long, linear chain, 5 nm in length, completely contained within a box 5.1 nm in length (i.e., not broken across periodic boundaries). If you try to calculate the end-to-end distance, you would want to get 5.0 nm. However, because that distance is larger than 2.5 nm, PLUMED assumes it has been broken across a boundary (even though it has not been), shifts atom positions to minimize that distance, and instead returns 0.1 nm. Obviously, that is not what you want. When this happens as a simulation progresses (as you unfold a protein, for example), you might see your end to end distance slowly increase, and then abruptly jump to a lower value, and then back up, and then back down, as PLUMED gets confused and tries to fix something that may or may not have been broken in the first place. 

In comes [WHOLEMOLECULES](https://www.plumed.org/doc-v2.5/user-doc/html/_w_h_o_l_e_m_o_l_e_c_u_l_e_s.html) and NOPBC. PLUMED has a function, called WHOLEMOLECULES, which explicitly rebuilds molecules that might have been broken across boundaries. You pass it in a list of atoms, and starting from the first atom in the list, it moves atom by atom, sequentially shifting the atomic positions so that each atom is the minimum image distance away from the previous atom. This (most of the time) rebuilds your molecule and makes it whole. You can thus put this command at the beginning of your PLUMED file, so that this process is done before any distances are measured. If you do this, you have to pass in the NOPBC flag to any of your distance/CV calculations, to turn off PLUMED's functionality of automatically applying the minimum image convention. The combination of WHOLEMOLECULES and NOPBC will hopefully fix most problems you run into.


    #The following WHOLEMOLECULES command explicitly rebuilds the whole chain, in case it was split across periodic boundaries.
    #See the linked paper for an explicit illustration of why this might be helpful
    WHOLEMOLECULES ENTITY0=1-201
    
    #Pass in the NOPBC flag to the DISTANCE calculation to turn off the automatic minimum image convention
    end_to_end_distance: DISTANCE ATOMS1,201 NOPBC

However, WHOLEMOLECULES itself can cause some non-obvious errors that you should be on the lookout for, particularly when you have more than one molecule/chain that you are trying to make whole (for example, ligand binding, dimer dissociation, etc). Look at the following PLUMED snippet:


    #Protein 1 is atoms 1-200, protein 2 is atoms 201-500. We rebuild both of them with the following command
    WHOLEMOLECULES ENTITY0=1-500
    
    #The following command returns an incorrect distance
    C_N_distance: DISTANCE ATOMS=200,201 NOPBC

  

Because WHOLEMOLECULES marches atom by atom down the list you give it, if your list of atoms is not actually continuous in physical space, it can lead to some pathological results. For example, if atom 200 is at the C-terminus of protein 1, and atom 201 is in the N-terminus of protein 2, these atoms might be quite far away from one another, even if the two proteins are interacting quite closely at their C-termini. WHOLEMOLECULES will likely shift the entirety of protein 2 to make atom 200 and 201 as close as possible, which is not what you wanted. You instead wanted them to still be relatively far apart, so that the C-termini can interact appropriately. As another example, imagine you tried to fix this problem by using two separate WHOLEMOLECULES commands - one for protein 1, and one for protein 2. This gets rid of the discontinuity in physical space issue. 


    #Protein 1 is atoms 1-200, protein 2 is atoms 201-500. We rebuild both of them with the following command
    WHOLEMOLECULES ENTITY0=1-200 ENTITY1=201-500
    
    #The following command could still return an incorrect distance if either of the proteins are split by a periodic boundary
    C_N_distance: DISTANCE ATOMS=200,201 NOPBC

  

However, imagine now that protein 2 is split by the periodic boundary - i.e. its C-terminus is in the middle of the cell, interacting with protein 1, while its N-terminus stretches beyond the edge of the cell, and wraps around the periodic boundary. Since we are building protein 2 _starting from its N-terminus_, the entirety of protein 2 will be shifted, as each subsequent atom after 201 is shifted to be as close as possible to the previous atom. Again, this gives a pathological result. One workaround is to play some games with how you pass in the lists that define the ENTITY in WHOLEMOLECULES, depending on the specific situation in your simulation. In this case, the C-termini are interacting in the middle of the cell, and its only the N-termini that are floating around near the edge of the cell, causing our pathological results. Thus, we can change the stride of the ENTITY to make it build each protein _from the C-terminus_. This makes sure that each protein is actually in the cell we want it to be in.


    #Protein 1 is atoms 1-200, protein 2 is atoms 201-500. We rebuild both of them (moving from C-terminus to N-terminus) with the following command
    #By adding the stride, we can change by how much we increment. Here, we are incrementing by -1, moving from C-terminus to N-terminus
    WHOLEMOLECULES ENTITY0=200-1:-1 ENTITY1=500-201:-1
    
    #The following command now returns the correct distance
    C_N_distance: DISTANCE ATOMS=200,201 NOPBC

  

You still should be careful, however. If now the C-termini stop interacting (if, for example, you are studying a dissociation), and float away far enough to be split by a periodic boundary, you would recover the same pathology as we had before. In this case, you might want to make your WHOLEMOLECULES command a bit more complex, so that it builds from some central atom that is never split across the boundary.

  

Overall, this process is complicated, and you should always be checking your output trajectories to make sure you aren't seeing pathological jumps in distances (or any collective variable that depends on a distance calculation, like contacts, RMSDs, etc.). You should be able to pass in the NOPBC flag to any calculation that depends on distances. 

**For more information, see section 2.7 of [this paper](https://link.springer.com/protocol/10.1007%2F978-1-4939-9608-7_21)**
