Concordia University

SOEN 6021 - Software Re-engineering

Converter from Scitools Understand .udb file to .ta file for lsedit

# Requirement
* [Scitool Understand](https://scitools.com/)
* Python
* Follow the configuration for using Python package with Scitool [here](https://scitools.com/support/python-api/)

# Usage
Using Scitool's Understand to analyze a source code. This will generate a `.udb` file.

Open the script, modify the path to `.udb` file, then run

```python
converter=understand_to_lsedit_converter()
converter.convert("demo\\nginx.udb","demo\\nginx_architecture.ta")
```