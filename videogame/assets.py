"""Game assets and where they are located. This is a lazy/OK solution 
to creating a singleton class."""

# This is kind of like a singleton class. It isn't a class though. It is a module.
# See discussion at
# https://stackoverflow.com/questions/6760685/what-is-the-best-way-of-implementing-singleton-in-python
# More information about the singleton design pattern is available on Wikipedia,
# https://en.wikipedia.org/wiki/Singleton_pattern.

from os import path
from .galaga_asset_dict import galaga_asset_dict as asset_dict

# The absolute path of the current file's directory
main_dir = path.split(path.abspath(__file__))[0]

# Path to the "music" folder inside your project
data_dir = path.abspath(path.join(main_dir, "..", "music"))

def get(key):
    """Given the key representing the asset, return a fully qualified path to the asset."""
    try:
        value = asset_dict[key]
    except KeyError:
        print(f'The asset key "{key}" is unknown and a KeyError exception was raised.')
        raise
    value = path.join(data_dir, value)
    assert path.exists(value), f"Asset not found: {value}"
    return value



