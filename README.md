Concordia University

SOEN 6021 - Software Re-engineering

Converter from Scitools Understand .udb file to .ta file for lsedit

# Requirement
* [Scitool Understand](https://scitools.com/)
* Python
* Follow the configuration for using Python package with Scitool [here](https://scitools.com/support/python-api/)

# Usage
Using Scitool's Understand to analyze a source code. This will generate a `.udb` file.

Open the script, modify the path to `.udb` file, then run the code

Example:

```python
converter=understand_to_lsedit_converter()
converter.convert("demo\\nginx.udb", "demo\\nginx_architecture.ta")
```

Open the `.ta` file in [lsedit](https://github.com/huntertran/lsedit), you will see something similar to this

![nginx folder structure](https://raw.githubusercontent.com/huntertran/udb-converter/master/demo/nginx_folder_structure.png)