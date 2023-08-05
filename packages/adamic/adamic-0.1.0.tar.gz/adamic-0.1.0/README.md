# adamic Package

## Overview

This package contains the code to build a data dictionary when passed a Pandas dataframe.

## Installation

This package is available on `pip`. To install, run the following from your preferred shell:
```sh
pip install adamic
```

## Use

After installing the package to your environment, import the package to your script, Jupyter notebook, or directly to the `python3` command line.

```py
from adamic import adamic
```

To create your data dictionary, pass a Pandas dataframe to the `create_data_dictionary()` function:

```py
adamic.create_data_dictionary(sample_df)
```

The package will prompt you to supply definitions for each variable in the dataset. Hit `Enter` after supplying definition or if you want to define the variable later after the output file has been created.

Finally, you will be prompted to name your preferred file extension. `.csv`, `.json`, and `.xlsx` are the available options.

## Credit

I've borrowed ideas for this package (especially the method of adding definitions) from [this Medium article](https://peter-easter-do.medium.com/creating-a-data-dictionary-with-python-cccb212e44dc). 