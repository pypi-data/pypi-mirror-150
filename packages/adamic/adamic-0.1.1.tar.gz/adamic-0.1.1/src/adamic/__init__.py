import os

with open(os.path.join(os.path.dirname(__file__),"VERSION")) as version_file:
    __version__ = version_file.read().strip()

__author__ = "Ben Moran"

## These functions and classes are public. 
## All other functions are functionally private.

from .adamic import _initialize_data_dictionary, _add_dictionary_definition
from .adamic import _output_dataframe, create_data_dictionary

__all__ = (
    "create_data_dictionary"
)


