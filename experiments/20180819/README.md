# B-mode image generator

William Meng K9TTL  
Aug 19, 2018

This script B_mode.py generates and displays a B-mode sector scan image
from a provided .npy file.

A lot of parameters are hardcoded in the default_params dictionary,
but at least they're not hardcoded in the function itself.
So now I just need a way to specify a custom params dictionary
based on some input from the command line.
Since there are lots of parameters, it would be messy to pass easy
parameter as a command line argument.
Instead, the user could pass the filename of some JSON data that
is then parsed to fill the dictionary.

Result:  
![image](Figure_1.png)
