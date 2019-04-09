# midas-extract

A library for subsetting CSV files from the MIDAS DB

* Free software: BSD - see LICENSE file in top-level package directory
* Documentation: https://midas-extract.readthedocs.io.

## Overview

Before using the code you will need to:

 - Install the package (within a python environment)
 - Set the MIDAS Data/Metadata directory environment directories
   - Required if NOT running on JASMIN

### Installation

Install from PyPI:

```
pip install midas_extract
```

Or from GitHub:

```
pip install git+https://github.com/cedadev/midas_extract
``` 

### If not on JASMIN: set your local data/metadata directories

If you are not on JASMIN then set these environment variables 
before you call the library:

```
export MIDAS_DATA_DIR=my-local-midas/data
export MIDAS_METADATA_DIR=my-local-midas/data
```

The defaults are set in the module:

 `midas_extract/settings.py`

## Using the library 

### Identify Weather Stations

Identifying weather stations at the command-line:



Identifying weather stations in Python:


### Subset Data Tables


Subsetting MIDAS data tables at the command-line:



Subsetting MIDAS data tables in Python:




# Credits

This package was created with `Cookiecutter` and the `audreyr/cookiecutter-pypackage` project template.

 * Cookiecutter: https://github.com/audreyr/cookiecutter
 * Cookiecutter PyPackage: https://github.com/audreyr/cookiecutter-pypackage
