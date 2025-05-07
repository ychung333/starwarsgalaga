"""
Game assets and where they are located. This is a lazy/OK solution 
to creating a singleton class.
"""

from os import path
from .galaga_asset_dict import galaga_asset_dict as asset_dict

# Get absolute path to this file's directory
main_dir = path.split(path.abspath(__file__))[0]

# Set path to the top-level "music" directory (outside /videogame/)
data_dir = path.abspath(path.join(main_dir, "..", "music"))

def get(key):
    """
    Given the key representing the asset, return a fully qualified path to the asset.
    """
    try:
        filename = asset_dict[key]
    except KeyError:
        print(f'Unknown asset key: "{key}"')
        raise

    full_path = path.join(data_dir, filename)

    # Ensure asset file exists
    assert path.exists(full_path), f"Asset not found: {full_path}"

    return full_path

