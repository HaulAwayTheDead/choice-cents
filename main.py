#!/usr/bin/env python3
"""
ChoiceCents: Your Money Journey
Main entry point for the game

Run this file to start playing!
"""

import sys
import os

# Add src directory to path so we can import game modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from enhanced_game_engine import EnhancedGameEngine

def main():
    """Main function to start the game"""
    try:
        # Use enhanced game engine with console interface
        game = EnhancedGameEngine(interface_type="console")
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user. Thanks for playing!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please report this bug to the developers.")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()