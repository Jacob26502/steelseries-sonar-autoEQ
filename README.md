﻿# steelseries-sonar-autoEQ
A thing I wrote.
## How to use
The script takes 2 arguments:

 - the path to the peace parametric configuration file (the file should look like this):
![image](https://user-images.githubusercontent.com/57222813/209248880-71133c6a-1de7-4fbf-876b-608c477db192.png)

If it's in the same dir, just use its name.

 - The name of a recently created Game profile on steelseries GG to be overwritten.

e.g 
```sh
python script.py "Audeze LCD-3 ParametricEQ.txt" "Configuration 1"
```
The script should be placed in the same directory as the "database.db" file that steelseries *SONAR* uses, which is located (by default) at "C:\ProgramData\SteelSeries\GG\apps\sonar\db\"

The above example has the default "new config" name, and the eq file in the same directory as the database and script.


Warning: was designed to be used on version 36.0.0, and has not been tested on later versions. I am not responsible if it breaks your Steelseries GG app. The script does make a backup before running just in case but don't trust it.

*UPDATE: Tested still working 83.1.0
