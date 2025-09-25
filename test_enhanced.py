"""
Simple test to verify ChoiceCents enhanced engine functionality
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import GameConfig, GameText
from ui_interface import create_interface
from enhanced_game_engine import GameState

def test_config():
    """Test configuration system"""
    print("Testing Configuration...")
    print(f"Game Title: {GameConfig.TITLE}")
    print(f"Version: {GameConfig.VERSION}")
    print(f"Starting Cash: ${GameConfig.STARTING_CASH}")
    print(f"Config Valid: {GameConfig.validate_config()}")
    print()

def test_ui():
    """Test UI interface"""
    print("Testing UI Interface...")
    ui = create_interface("console")
    
    ui.display_text("This is a test message", "normal")
    ui.display_text("This is a success message", "success")
    ui.display_text("This is a warning message", "warning")
    ui.display_text("This is an error message", "error")
    
    ui.display_separator()
    
    # Test financial status display
    test_status = {
        'age': 18,
        'month': 1,
        'cash': 1000.0,
        'monthly_income': 0,
        'education_debt': 0,
        'savings_account': 0,
        'net_worth': 1000.0,
        'credit_score': 650,
        'wellbeing_score': 50
    }
    
    ui.display_financial_status(test_status)
    print()

def test_game_state():
    """Test game state functionality"""
    print("Testing Game State...")
    state = GameState()
    
    print(f"Player starts with ${state.cash}")
    print(f"Net worth: ${state.get_net_worth()}")
    print(f"Monthly cash flow: ${state.get_monthly_cash_flow()}")
    
    # Test achievements
    state.monthly_income = 2000
    new_achievements = state.check_achievements()
    print(f"New achievements: {new_achievements}")
    print()

def main():
    """Run all tests"""
    print("=" * 50)
    print("ChoiceCents Enhanced Engine Test")
    print("=" * 50)
    
    test_config()
    test_ui()
    test_game_state()
    
    print("All tests completed!")
    print("If you see this message, the enhanced engine is ready to run.")
    print("\nTo play the game, run: python main.py")

if __name__ == "__main__":
    main()