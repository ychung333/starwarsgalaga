#!/usr/bin/env python3
"""
Entry point for the Galaga-style game.
"""

from videogame.game import GalagaGame

def main():
    """
    Start the Galaga-style game.
    """
    game = GalagaGame()
    game.run()

if __name__ == "__main__":
    main()
