"""
ChoiceCents Configuration Module
Centralized settings and constants for the game
"""

import os
from typing import Dict, Any

class GameConfig:
    """Central configuration for ChoiceCents game"""
    
    # Game Version
    VERSION = "0.1.0-MVP"
    TITLE = "ChoiceCents: Your Money Journey"
    
    # File Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    SAVES_DIR = os.path.join(BASE_DIR, "saves")
    
    # Game Balance Settings
    STARTING_CASH = 1000.0
    STARTING_CREDIT_SCORE = 650
    STARTING_WELLBEING = 50
    STARTING_AGE = 18
    
    # Financial Constants (Indiana-based)
    EDUCATION_COSTS = {
        "four_year_college": 40000,
        "community_college": 15000,
        "trade_school": 13000,
        "military": 0,
        "immediate_work": 0,
        "entrepreneur": 5000  # startup costs
    }
    
    STARTING_SALARIES = {
        "four_year_college": 0,  # No immediate income
        "community_college": 0,  # No immediate income
        "trade_school": 0,       # No immediate income
        "military": 2200,
        "immediate_work": 2400,
        "entrepreneur": 1500     # Variable income
    }
    
    # Living Costs (Monthly, Indiana averages)
    LIVING_COSTS = {
        "housing_student": 800,
        "housing_shared": 600,
        "housing_studio": 1000,
        "food_basic": 300,
        "transport_public": 80,
        "transport_car": 200,
        "utilities": 120,
        "phone": 50,
        "insurance_basic": 150
    }
    
    # Game Mechanics
    RANDOM_EVENT_CHANCE = 0.10    # 10% chance per month
    MINIGAME_CHANCE = 0.15        # 15% chance per month
    DEBT_INTEREST_RATE = 0.048    # 4.8% annual student loan interest
    CREDIT_SCORE_RANGE = (300, 850)
    WELLBEING_RANGE = (0, 100)
    
    # Progression Settings
    MONTHS_PER_CHAPTER = 12
    TOTAL_CHAPTERS = 4
    MAX_LIFE_GOALS = 3
    
    # Display Settings (for future GUI)
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600
    FONT_SIZE_NORMAL = 12
    FONT_SIZE_LARGE = 16
    FONT_SIZE_TITLE = 24
    
    # Colors (for future GUI)
    COLORS = {
        "primary": "#2E8B57",      # Sea Green
        "secondary": "#FFD700",    # Gold
        "background": "#F5F5F5",   # White Smoke
        "text": "#333333",         # Dark Gray
        "success": "#28A745",      # Green
        "warning": "#FFC107",      # Amber
        "danger": "#DC3545",       # Red
        "info": "#17A2B8"          # Cyan
    }
    
    # Text Interface Settings (current)
    TEXT_WIDTH = 60
    SEPARATOR_CHAR = "="
    
    @classmethod
    def get_data_file_path(cls, filename: str) -> str:
        """Get the full path to a data file"""
        return os.path.join(cls.DATA_DIR, filename)
    
    @classmethod
    def get_save_file_path(cls, filename: str) -> str:
        """Get the full path to a save file"""
        return os.path.join(cls.SAVES_DIR, filename)
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        for directory in [cls.DATA_DIR, cls.SAVES_DIR]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        try:
            # Check critical paths exist
            if not os.path.exists(cls.BASE_DIR):
                print(f"Warning: Base directory not found: {cls.BASE_DIR}")
                return False
            
            # Ensure directories are created
            cls.ensure_directories()
            
            # Validate numeric ranges
            if cls.STARTING_CREDIT_SCORE < cls.CREDIT_SCORE_RANGE[0] or \
               cls.STARTING_CREDIT_SCORE > cls.CREDIT_SCORE_RANGE[1]:
                print("Warning: Starting credit score outside valid range")
                return False
            
            if cls.STARTING_WELLBEING < cls.WELLBEING_RANGE[0] or \
               cls.STARTING_WELLBEING > cls.WELLBEING_RANGE[1]:
                print("Warning: Starting wellbeing score outside valid range")
                return False
            
            return True
            
        except Exception as e:
            print(f"Configuration validation error: {e}")
            return False


# Game Text Constants
class GameText:
    """Text constants for the game interface"""
    
    WELCOME_MESSAGE = f"""
{GameConfig.SEPARATOR_CHAR * GameConfig.TEXT_WIDTH}
    {GameConfig.TITLE}
    A Personal Finance Adventure Game
{GameConfig.SEPARATOR_CHAR * GameConfig.TEXT_WIDTH}

Welcome to ChoiceCents! In this game, you'll make
financial decisions that will shape your life journey.
Learn about budgeting, saving, investing, and more
as you navigate from high school graduation to retirement.

Your choices matter - let's begin your money journey!
"""
    
    MAIN_MENU = """
========================================
MAIN MENU
========================================
1. New Game
2. Load Game
3. About
4. Quit
"""
    
    CHARACTER_CREATION_HEADER = """
========================================
CHARACTER CREATION
========================================
"""
    
    CHAPTER_1_INTRO = """
==================================================
CHAPTER 1: GRADUATION DAY
==================================================

Congratulations! You've graduated high school.
Now you need to decide what to do next.
Each path has different costs, benefits, and opportunities.
"""
    
    LIFE_GOALS_OPTIONS = [
        "Buy a car",
        "Get a college degree", 
        "Buy a house",
        "Start a family",
        "Travel the world",
        "Retire early",
        "Start a business",
        "Build an emergency fund",
        "Pay off all debt",
        "Achieve financial independence"
    ]
    
    EDUCATION_PATHS = {
        "1": {
            "name": "Four-year college",
            "description": "Bachelor's degree - higher earning potential but significant debt",
            "debt": GameConfig.EDUCATION_COSTS["four_year_college"],
            "time_years": 4,
            "immediate_income": 0
        },
        "2": {
            "name": "Community college/Trade school", 
            "description": "Practical skills, lower debt, faster entry to workforce",
            "debt": GameConfig.EDUCATION_COSTS["community_college"],
            "time_years": 2,
            "immediate_income": 0
        },
        "3": {
            "name": "Enter workforce immediately",
            "description": "Start earning right away, no debt, but limited growth",
            "debt": 0,
            "time_years": 0,
            "immediate_income": GameConfig.STARTING_SALARIES["immediate_work"]
        },
        "4": {
            "name": "Join the military",
            "description": "Steady pay, benefits, and education opportunities",
            "debt": 0,
            "time_years": 4,
            "immediate_income": GameConfig.STARTING_SALARIES["military"]
        },
        "5": {
            "name": "Start your own business",
            "description": "High risk, high reward, unlimited potential",
            "debt": 0,
            "startup_cost": GameConfig.EDUCATION_COSTS["entrepreneur"],
            "immediate_income": GameConfig.STARTING_SALARIES["entrepreneur"]
        }
    }


# Achievement System (for gamification)
class Achievements:
    """Achievement definitions for the game"""
    
    ACHIEVEMENT_LIST = {
        "first_dollar": {
            "name": "First Dollar Earned",
            "description": "Earn your first paycheck",
            "condition": "monthly_income > 0",
            "reward_wellbeing": 5
        },
        "emergency_fund": {
            "name": "Emergency Cushion",
            "description": "Save $1,000 in emergency fund",
            "condition": "savings_account >= 1000",
            "reward_wellbeing": 10
        },
        "debt_free": {
            "name": "Debt Free",
            "description": "Pay off all your debt",
            "condition": "education_debt <= 0",
            "reward_wellbeing": 15
        },
        "investor": {
            "name": "Future Investor",
            "description": "Make your first investment",
            "condition": "sum(investments.values()) > 0",
            "reward_wellbeing": 8
        },
        "high_credit": {
            "name": "Credit Master",
            "description": "Achieve a credit score over 750",
            "condition": "credit_score >= 750",
            "reward_wellbeing": 12
        },
        "net_worth_positive": {
            "name": "Positive Net Worth",
            "description": "Achieve positive net worth",
            "condition": "get_net_worth() > 0",
            "reward_wellbeing": 10
        }
    }


if __name__ == "__main__":
    # Test configuration
    print(f"ChoiceCents Configuration v{GameConfig.VERSION}")
    print(f"Base Directory: {GameConfig.BASE_DIR}")
    print(f"Configuration Valid: {GameConfig.validate_config()}")
    
    # Display some sample text
    print(GameText.WELCOME_MESSAGE)