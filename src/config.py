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
        "housing_student_dorm": 900,
        "housing_student_shared": 650,
        "housing_young_professional": 800,
        "housing_studio": 1000,
        "housing_one_bedroom": 1200,
        "housing_family_rental": 1600,
        "food_basic": 300,
        "food_moderate": 450,
        "food_premium": 600,
        "transport_public": 80,
        "transport_bicycle": 20,      # Bike maintenance/gear
        "transport_used_car": 250,    # Payment + insurance + gas
        "transport_reliable_car": 400,
        "transport_new_car": 550,
        "utilities_basic": 120,
        "utilities_full": 180,
        "phone_basic": 35,
        "phone_premium": 85,
        "insurance_basic": 150,
        "insurance_comprehensive": 250,
        "entertainment_minimal": 50,
        "entertainment_moderate": 150,
        "entertainment_high": 300,
        "clothing_basic": 50,
        "clothing_professional": 100
    }
    
    # Vehicle Options
    VEHICLE_OPTIONS = {
        "none": {
            "name": "No Vehicle",
            "monthly_cost": 0,
            "purchase_cost": 0,
            "reliability": 100,  # Public transport is reliable
            "description": "Rely on public transportation, walking, and rides"
        },
        "bicycle": {
            "name": "Bicycle",
            "monthly_cost": 20,
            "purchase_cost": 400,
            "reliability": 85,
            "description": "Eco-friendly, healthy, but weather dependent"
        },
        "old_car": {
            "name": "Old Used Car ($3,000)",
            "monthly_cost": 180,  # Insurance, gas, maintenance
            "purchase_cost": 3000,
            "reliability": 60,
            "description": "Cheap but potentially unreliable"
        },
        "reliable_used": {
            "name": "Reliable Used Car ($8,000)",
            "monthly_cost": 220,
            "purchase_cost": 8000,
            "reliability": 85,
            "description": "Good balance of cost and reliability"
        },
        "certified_pre_owned": {
            "name": "Certified Pre-owned ($15,000)",
            "monthly_cost": 320,
            "purchase_cost": 15000,
            "reliability": 95,
            "description": "Nearly new reliability with warranty"
        },
        "new_car": {
            "name": "New Car ($25,000)",
            "monthly_cost": 450,
            "purchase_cost": 25000,
            "reliability": 98,
            "description": "Latest features and full warranty"
        },
        "luxury_car": {
            "name": "Luxury Car ($40,000)",
            "monthly_cost": 650,
            "purchase_cost": 40000,
            "reliability": 95,
            "description": "Premium features but higher costs"
        }
    }
    
    # Game Mechanics
    RANDOM_EVENT_CHANCE = 0.08    # 8% chance per month (reduced due to more content)
    MINIGAME_CHANCE = 0.12        # 12% chance per month
    CAREER_EVENT_CHANCE = 0.06    # 6% chance for career-related events
    DEBT_INTEREST_RATE = 0.048    # 4.8% annual student loan interest
    CREDIT_SCORE_RANGE = (300, 850)
    WELLBEING_RANGE = (0, 100)
    
    # Time Scaling
    TIME_SKIP_OPTIONS = [1, 3, 6]  # Months that can be skipped at once
    AUTO_SKIP_THRESHOLD = 0.05     # If monthly change < 5%, suggest time skip
    
    # Progression Settings
    MONTHS_PER_CHAPTER = 24        # Increased for more depth
    TOTAL_CHAPTERS = 6             # Extended life simulation
    MAX_LIFE_GOALS = 5             # Allow more goals
    
    # Part-time Work
    PART_TIME_INCOME_RANGE = (800, 1500)  # Monthly part-time income
    PART_TIME_WELLBEING_COST = 10          # Stress from working while studying
    STUDY_TIME_IMPACT = 0.1                # GPA impact from part-time work
    SIMULATION_LENGTH_MONTHS = 36          # 3 year simulation
    
    # Part-time job wages (monthly estimates for part-time work)
    PART_TIME_JOB_WAGES = {
        "retail": 1200,
        "food_service": 1000,
        "tutoring": 1500,
        "office_assistant": 1300,
        "campus_job": 800,
        "freelance": 1400
    }
    
    # Part-time job details
    PART_TIME_JOBS = {
        "retail": {
            "title": "Retail Sales Associate",
            "hourly_wage": 15,
            "max_hours_per_week": 20,
            "education_compatible": ["Community College", "4-Year University", "Trade School"],
            "skills_developed": ["customer service", "sales"]
        },
        "food_service": {
            "title": "Food Service Worker",
            "hourly_wage": 12,
            "max_hours_per_week": 25,
            "education_compatible": ["Community College", "4-Year University", "Trade School"],
            "skills_developed": ["teamwork", "time management"]
        },
        "tutoring": {
            "title": "Peer Tutor",
            "hourly_wage": 18,
            "max_hours_per_week": 15,
            "education_compatible": ["4-Year University"],
            "skills_developed": ["communication", "subject expertise"]
        },
        "office_assistant": {
            "title": "Office Assistant",
            "hourly_wage": 14,
            "max_hours_per_week": 20,
            "education_compatible": ["Community College", "4-Year University"],
            "skills_developed": ["organization", "computer skills"]
        },
        "campus_job": {
            "title": "Campus Work-Study",
            "hourly_wage": 10,
            "max_hours_per_week": 20,
            "education_compatible": ["Community College", "4-Year University"],
            "skills_developed": ["responsibility", "campus knowledge"]
        },
        "freelance": {
            "title": "Freelance Work",
            "hourly_wage": 20,
            "max_hours_per_week": 15,
            "education_compatible": ["Community College", "4-Year University", "Trade School"],
            "skills_developed": ["entrepreneurship", "self-management"]
        }
    }
    
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
        "Buy a reliable car",
        "Get a college degree", 
        "Buy a house",
        "Start a family",
        "Travel internationally",
        "Retire early (before 60)",
        "Start a successful business",
        "Build a 6-month emergency fund",
        "Pay off all debt",
        "Achieve financial independence",
        "Own a luxury car",
        "Buy investment property",
        "Start a charitable foundation",
        "Live debt-free lifestyle",
        "Build a diversified investment portfolio"
    ]
    
    EDUCATION_PATHS = {
        "1": {
            "name": "Four-year university (Public)",
            "description": "Bachelor's degree at state university - good ROI",
            "debt": 35000,
            "time_years": 4,
            "immediate_income": 0,
            "allows_part_time": True,
            "gpa_requirement": 2.0
        },
        "2": {
            "name": "Four-year university (Private)",
            "description": "Bachelor's degree at private college - premium education",
            "debt": 60000,
            "time_years": 4,
            "immediate_income": 0,
            "allows_part_time": True,
            "gpa_requirement": 2.5
        },
        "3": {
            "name": "Community college",
            "description": "Associate degree - affordable and practical",
            "debt": 8000,
            "time_years": 2,
            "immediate_income": 0,
            "allows_part_time": True,
            "gpa_requirement": 2.0
        },
        "4": {
            "name": "Trade school",
            "description": "Specialized skills training - fast track to employment",
            "debt": 15000,
            "time_years": 1.5,
            "immediate_income": 0,
            "allows_part_time": False,  # Too intensive
            "gpa_requirement": None
        },
        "5": {
            "name": "Enter workforce immediately",
            "description": "Start earning right away, no debt, but limited growth",
            "debt": 0,
            "time_years": 0,
            "immediate_income": GameConfig.STARTING_SALARIES["immediate_work"],
            "allows_part_time": False,
            "gpa_requirement": None
        },
        "6": {
            "name": "Join the military",
            "description": "Steady pay, benefits, and education opportunities",
            "debt": 0,
            "time_years": 4,
            "immediate_income": GameConfig.STARTING_SALARIES["military"],
            "allows_part_time": False,
            "gpa_requirement": None
        },
        "7": {
            "name": "Start your own business",
            "description": "High risk, high reward, unlimited potential",
            "debt": 0,
            "startup_cost": GameConfig.EDUCATION_COSTS["entrepreneur"],
            "immediate_income": GameConfig.STARTING_SALARIES["entrepreneur"],
            "allows_part_time": False,
            "gpa_requirement": None
        },
        "8": {
            "name": "Gap year + travel",
            "description": "Take a year to explore, work, and figure out your path",
            "debt": 0,
            "time_years": 1,
            "immediate_income": 1800,  # Part-time/seasonal work
            "allows_part_time": True,
            "gpa_requirement": None
        }
    }
    
    # Part-time Job Options (available during education)
    PART_TIME_JOBS = {
        "retail": {
            "name": "Retail Associate",
            "hourly_wage": 12,
            "hours_per_week": 20,
            "flexibility": "high",
            "skill_building": "customer service",
            "description": "Work in stores, flexible scheduling"
        },
        "food_service": {
            "name": "Food Service Worker",
            "hourly_wage": 11,
            "hours_per_week": 25,
            "flexibility": "medium",
            "skill_building": "teamwork",
            "description": "Restaurant/cafeteria work, includes tips"
        },
        "tutor": {
            "name": "Tutor",
            "hourly_wage": 18,
            "hours_per_week": 15,
            "flexibility": "high",
            "skill_building": "communication",
            "description": "Help other students, great for resume"
        },
        "office_assistant": {
            "name": "Office Assistant",
            "hourly_wage": 15,
            "hours_per_week": 20,
            "flexibility": "medium",
            "skill_building": "professional skills",
            "description": "Administrative work, office experience"
        },
        "delivery": {
            "name": "Delivery Driver",
            "hourly_wage": 14,
            "hours_per_week": 20,
            "flexibility": "high",
            "skill_building": "time management",
            "description": "Food/package delivery, need reliable vehicle"
        },
        "freelance": {
            "name": "Freelance Work",
            "hourly_wage": 22,
            "hours_per_week": 12,
            "flexibility": "very high",
            "skill_building": "entrepreneurship",
            "description": "Writing, design, programming - build portfolio"
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
        "part_time_worker": {
            "name": "Juggling Act",
            "description": "Successfully balance work and studies",
            "condition": "has_part_time_job and is_student",
            "reward_wellbeing": 8
        },
        "emergency_fund_starter": {
            "name": "Emergency Cushion",
            "description": "Save $1,000 in emergency fund",
            "condition": "savings_account >= 1000",
            "reward_wellbeing": 10
        },
        "emergency_fund_master": {
            "name": "Prepared for Anything",
            "description": "Save 6 months of expenses",
            "condition": "savings_account >= monthly_expenses * 6",
            "reward_wellbeing": 20
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
        "diversified_investor": {
            "name": "Portfolio Builder",
            "description": "Invest in 3+ different asset types",
            "condition": "len([v for v in investments.values() if v > 0]) >= 3",
            "reward_wellbeing": 15
        },
        "high_credit": {
            "name": "Credit Master",
            "description": "Achieve a credit score over 750",
            "condition": "credit_score >= 750",
            "reward_wellbeing": 12
        },
        "excellent_credit": {
            "name": "Credit Superstar",
            "description": "Achieve a credit score over 800",
            "condition": "credit_score >= 800",
            "reward_wellbeing": 18
        },
        "net_worth_positive": {
            "name": "Positive Net Worth",
            "description": "Achieve positive net worth",
            "condition": "get_net_worth() > 0",
            "reward_wellbeing": 10
        },
        "net_worth_10k": {
            "name": "Building Wealth",
            "description": "Reach $10,000 net worth",
            "condition": "get_net_worth() >= 10000",
            "reward_wellbeing": 15
        },
        "net_worth_50k": {
            "name": "Wealth Accumulator",
            "description": "Reach $50,000 net worth",
            "condition": "get_net_worth() >= 50000",
            "reward_wellbeing": 25
        },
        "car_owner": {
            "name": "Mobile Independence",
            "description": "Purchase your first car",
            "condition": "owns_vehicle and vehicle_type != 'none'",
            "reward_wellbeing": 12
        },
        "smart_shopper": {
            "name": "Value Hunter",
            "description": "Complete 5 comparison shopping challenges",
            "condition": "comparison_shopping_wins >= 5",
            "reward_wellbeing": 10
        },
        "budget_master": {
            "name": "Budget Master",
            "description": "Stay within budget for 6 consecutive months",
            "condition": "consecutive_budget_months >= 6",
            "reward_wellbeing": 18
        },
        "side_hustler": {
            "name": "Side Hustler",
            "description": "Earn money from multiple income sources",
            "condition": "income_sources >= 2",
            "reward_wellbeing": 12
        }
    }


if __name__ == "__main__":
    # Test configuration
    print(f"ChoiceCents Configuration v{GameConfig.VERSION}")
    print(f"Base Directory: {GameConfig.BASE_DIR}")
    print(f"Configuration Valid: {GameConfig.validate_config()}")
    
    # Display some sample text
    print(GameText.WELCOME_MESSAGE)