# [MD_VMD]- Expected-integer-but-got-08 -Error-When-Running-TCL-Script.md
Problem
-------

According to this error, 8 is not a number. Which can be frustrating, because all of you prior experience likely suggests to you that 8 is, in fact, a number. This is because tcl scripts by default assume [any number with leading zeros is an octal number](https://wiki.tcl-lang.org/page/Tcl+and+octal+numbers), meaning any integer that contains either an 8 or 9 is not a valid octal number. You cannot perform any time of arithmetic operations on these "invalid" numbers. 

Solution
--------

If you need to manipulate any numbers with padding zeros, use scan as illustrated in [this article ](https://wiki.tcl-lang.org/page/Tcl+and+octal+numbers) to get rid of them, and convert back to a normal base-10 number. You can then re-add the padding zeros by running something like the following command: `set PADDED [format "%03d" $NOT_PADDED]`. Alternatively, you could do all your manipulation before calling VMD, and only pass in the padded number to be used as a string.

