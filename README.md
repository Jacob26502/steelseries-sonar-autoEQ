# steelseries-sonar-autoEQ
A thing I wrote.
## How to use
The script takes 2 arguments:

 - the relative path of the peace parametric configuration file (they should look like this):
![image](https://user-images.githubusercontent.com/57222813/209248880-71133c6a-1de7-4fbf-876b-608c477db192.png)

If it's in the same dir, just use its name.

 - The name of a recently created Game profile on steelseries GG to be overwritten.

e.g 
```sh
python script.py "Audeze LCD-3 ParametricEQ.txt" "Configuration 1"
```
The script should be placed in the same directory as the "database.db" file that steelseries *SONAR* uses, which is located (by default) at "C:\ProgramData\SteelSeries\GG\apps\sonar\db\"

The above example has the default "new config" name, and the eq file in the same directory as the database and script.


