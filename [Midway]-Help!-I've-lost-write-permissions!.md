Problem
-------

You can no longer save or write any files, or maybe you aren't even allowed to log on at all. 

Solution
--------

You have likely gone over your file size or file limit quota. Type 

`rcchelp quota`

to see what systems you have access to, and see if you are over any of your limits. You should never exceed your quota in your /home directory - as a general rule, never actually save anything there, at least nothing substantial. Make sure everything is on /scratch, /project2, or /cds. If your are over limits on any of these systems, you will likely need to coordinate with other lab members to delete files. If you need to transfer large numbers of files, or very large files/directories, you should  **absolutely ** be using [Globus](https://globus.rcc.uchicago.edu/) - it is extraordinarily fast, and doesn't hog the login node/interactive session. While you _can_ constantly shuffle files around to take advantage of the 30 day grace period on scratch, this behavior is discouraged.
