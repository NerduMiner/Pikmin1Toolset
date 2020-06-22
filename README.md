# Pikmin1Toolset
A collection of tools for Pikmin 1.  This includes mod2obj, obj2mod

# Requirements
- `pillow`
- `bitstring`

# mod2obj
Converts nonrigged .MOD files into .obj or .ply models
## Usage
### Windows
Drag and drop the .mod file onto mod2obj.bat
### Linux
Open terminal and type
```
./mod2obj.sh {.mod file here}
```

# obj2mod
Converts an obj into a .mod file, requires a donor .mod to add sections that can't be created at this time with the program
NOTE: While it does create a .mod file, it will crash Pikmin 1 due to discrepancies with certain sections
## Usage
### Windows
Open cmd and type
```
__obj2mod.bat {obj file} {mod file} {ini file}
```
### Linux
Open terminal and type
```
./obj2mod.sh {obj file} {mod file} {ini file}
```

# Cleaning Up
If you need to clean up the directory of files outputted when running the programs, run the equivilant cleanup script based on
your system
NOTE: Take care when using this as it may delete files you may want to keep.
