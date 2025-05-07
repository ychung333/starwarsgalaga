"""
Game assets and where they are located.
"""

from os import path
from .galaga_asset_dict import galaga_asset_dict as asset_dict

# Get absolute path to this file's directory
main_dir = path.split(path.abspath(__file__))[0]

def get(key):
    """
    Given the key representing the asset, return a fully qualified path to the asset.
    Supports both 'music/' and 'ships/' assets.
    """
    try:
        relative_path = asset_dict[key]
    except KeyError:
        print(f'Unknown asset key: "{key}"')
        raise

    # Get the top-level project directory
    project_dir = path.abspath(path.join(main_dir, ".."))

    # Build full path to the asset (e.g., ships/player.png or music/gameplay.wav)
    full_path = path.join(project_dir, relative_path)

    assert path.exists(full_path), f"Asset not found: {full_path}"
    return full_path

