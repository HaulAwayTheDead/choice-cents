"""
ChoiceCents: Your Money Journey
A text-based personal finance education game

Core Game Engine
"""

import json
import os
import sys
import random
from datetime import datetime
from typing import Dict, Any, List, Optional
from minigames import ComparisonShoppingGame, BudgetAllocationGame, InvestmentSimulationGame, get_random_minigame

class GameState:
    """Manages the player's current game state"""
    
    def __init__(self):
        # Player Information
        self.player_name: str = ""
        self.player_age: int = 18
        self.current_chapter: int = 1
        self.game_month: int = 0
        
        # Financial State
        self.cash: float = 1000.0  # Starting cash
        self.monthly_income: float = 0.0
        self.monthly_expenses: Dict[str, float] = {
            "housing": 0.0,
            "food": 0.0,
            "transportation": 0.0,
            "entertainment": 0.0,
            "savings": 0.0,
            "debt_payments": 0.0,
            "taxes": 0.0,
            "insurance": 0.0,
            "other": 0.0
        }
        
        # Career and Education
        self.education_path: str = ""
        self.career: str = ""
        self.education_debt: float = 0.0
        self.credit_score: int = 650  # Starting credit score
        
        # Assets and Investments
        self.savings_account: float = 0.0
        self.investments: Dict[str, float] = {
            "stocks": 0.0,
            "bonds": 0.0,
            "index_funds": 0.0,
            "retirement_401k": 0.0
        }
        
        # Life Goals and Well-being
        self.life_goals: List[str] = []
        self.wellbeing_score: int = 50  # Scale of 0-100
        self.goals_completed: List[str] = []
        
        # Game Metadata
        self.save_date: str = ""
        self.total_playtime: int = 0  # in minutes
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert game state to dictionary for saving"""
        return {
            "player_name": self.player_name,
            "player_age": self.player_age,
            "current_chapter": self.current_chapter,
            "game_month": self.game_month,
            "cash": self.cash,
            "monthly_income": self.monthly_income,
            "monthly_expenses": self.monthly_expenses,
            "education_path": self.education_path,
            "career": self.career,
            "education_debt": self.education_debt,
            "credit_score": self.credit_score,
            "savings_account": self.savings_account,
            "investments": self.investments,
            "life_goals": self.life_goals,
            "wellbeing_score": self.wellbeing_score,
            "goals_completed": self.goals_completed,
            "save_date": self.save_date,
            "total_playtime": self.total_playtime
        }
    
    def from_dict(self, data: Dict[str, Any]):
        """Load game state from dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def get_net_worth(self) -> float:
        """Calculate total net worth"""
        assets = (self.cash + self.savings_account + 
                 sum(self.investments.values()))
        debts = self.education_debt
        return assets - debts
    
    def get_monthly_cash_flow(self) -> float:
        """Calculate monthly cash flow (income - expenses)"""
        total_expenses = sum(self.monthly_expenses.values())
        return self.monthly_income - total_expenses


class GameEngine:
    """Main game engine that manages game flow and state"""
    
    def __init__(self):
        self.state = GameState()
        self.running = True
        self.save_directory = "saves"
        
        # Ensure save directory exists
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
    
    def display_welcome(self):
        """Display welcome message and game introduction"""
        print("=" * 60)
        print("    ChoiceCents: Your Money Journey")
        print("    A Personal Finance Adventure Game")
        print("=" * 60)
        print()
        print("Welcome to ChoiceCents! In this game, you'll make")
        print("financial decisions that will shape your life journey.")
        print("Learn about budgeting, saving, investing, and more")
        print("as you navigate from high school graduation to retirement.")
        print()
        print("Your choices matter - let's begin your money journey!")
        print()
    
    def get_player_input(self, prompt: str, valid_options: Optional[List[str]] = None) -> str:
        """Get validated input from player"""
        while True:
            response = input(prompt).strip().lower()
            
            if valid_options is None:
                return response
            
            if response in [option.lower() for option in valid_options]:
                # Return the original case version
                for option in valid_options:
                    if response == option.lower():
                        return option
            
            print(f"Please enter one of: {', '.join(valid_options)}")
    
    def display_main_menu(self):
        """Display main menu options"""
        print("\n" + "=" * 40)
        print("MAIN MENU")
        print("=" * 40)
        print("1. New Game")
        print("2. Load Game")
        print("3. Quit")
        print()
        
        choice = self.get_player_input("Choose an option (1-3): ", ["1", "2", "3"])
        return choice
    
    def new_game(self):
        """Start a new game"""
        print("\n" + "=" * 40)
        print("CHARACTER CREATION")
        print("=" * 40)
        
        # Get player name
        while True:
            name = input("What's your name? ").strip()
            if name:
                self.state.player_name = name
                break
            print("Please enter a name.")
        
        print(f"\nHello, {self.state.player_name}!")
        print("You're 18 years old and about to graduate high school.")
        print("It's time to make some important decisions about your future!")
        
        # Set initial life goals
        print("\nWhat are your main life goals? (Choose up to 3)")
        goals_options = [
            "Buy a car",
            "Get a college degree",
            "Buy a house",
            "Start a family",
            "Travel the world",
            "Retire early",
            "Start a business",
            "Build an emergency fund"
        ]
        
        for i, goal in enumerate(goals_options, 1):
            print(f"{i}. {goal}")
        
        print("\nEnter the numbers of your chosen goals (e.g., 1,3,5):")
        while True:
            try:
                goal_nums = input().strip().split(',')
                goal_nums = [int(num.strip()) for num in goal_nums if num.strip()]
                
                if len(goal_nums) <= 3 and all(1 <= num <= len(goals_options) for num in goal_nums):
                    self.state.life_goals = [goals_options[num-1] for num in goal_nums]
                    break
                else:
                    print("Please enter up to 3 valid numbers.")
            except ValueError:
                print("Please enter numbers separated by commas.")
        
        print(f"\nGreat! Your goals are: {', '.join(self.state.life_goals)}")
        print("Remember these as you make decisions - they'll guide your journey!")
        
        # Start the game
        self.start_chapter_1()
    
    def start_chapter_1(self):
        """Chapter 1: High School Graduation - Choose Your Path"""
        print("\n" + "=" * 50)
        print("CHAPTER 1: GRADUATION DAY")
        print("=" * 50)
        print()
        print("Congratulations! You've graduated high school.")
        print("Now you need to decide what to do next.")
        print("Each path has different costs, benefits, and opportunities.")
        print()
        
        print("Your options:")
        print("1. Four-year college (Bachelor's degree)")
        print("2. Community college / Trade school")
        print("3. Enter the workforce immediately")
        print("4. Join the military")
        print("5. Start your own business")
        print()
        
        choice = self.get_player_input("What path will you choose? (1-5): ", 
                                     ["1", "2", "3", "4", "5"])
        
        self.process_education_choice(choice)
    
    def process_education_choice(self, choice: str):
        """Process the player's education/career path choice"""
        if choice == "1":
            self.state.education_path = "Four-year college"
            self.state.education_debt = 40000  # Average student loan debt
            self.state.cash -= 2000  # Initial costs
            print(f"\nYou've chosen to attend a four-year university!")
            print("This will take 4 years and cost about $40,000 in student loans.")
            print("But you'll have access to higher-paying careers afterward.")
            
        elif choice == "2":
            self.state.education_path = "Community college/Trade school"
            self.state.education_debt = 15000  # Lower debt
            self.state.cash -= 1000
            print(f"\nYou've chosen community college or trade school!")
            print("This will take 2 years and cost about $15,000.")
            print("You'll learn practical skills and enter the workforce sooner.")
            
        elif choice == "3":
            self.state.education_path = "High school diploma"
            self.state.monthly_income = 2400  # Entry-level job
            print(f"\nYou've chosen to start working right away!")
            print("You'll begin earning $2,400/month at an entry-level job.")
            print("No debt, but potentially limited career growth.")
            
        elif choice == "4":
            self.state.education_path = "Military service"
            self.state.monthly_income = 2200  # Military pay
            print(f"\nYou've enlisted in the military!")
            print("You'll earn $2,200/month plus benefits and training.")
            print("The military will pay for your education afterward.")
            
        elif choice == "5":
            self.state.education_path = "Entrepreneur"
            self.state.cash -= 5000  # Startup costs
            self.state.monthly_income = 1500  # Variable income
            print(f"\nYou've decided to start your own business!")
            print("You've invested $5,000 of your savings.")
            print("Income is unpredictable but has unlimited potential!")
        
        # Continue to first month simulation
        self.simulate_month()
    
    def simulate_month(self):
        """Simulate one month of financial decisions"""
        self.state.game_month += 1
        
        print(f"\n" + "=" * 50)
        print(f"MONTH {self.state.game_month}")
        print("=" * 50)
        
        # Display current financial status
        self.display_financial_status()
        
        # If player has income, do budgeting
        if self.state.monthly_income > 0:
            self.monthly_budgeting()
        
        # Random events (10% chance)
        if random.random() < 0.1:
            self.random_event()
        
        # Mini-games (15% chance)
        if random.random() < 0.15:
            self.play_random_minigame()
        
        # Update cash based on cash flow
        cash_flow = self.state.get_monthly_cash_flow()
        self.state.cash += cash_flow
        
        # Check for debt payments
        if self.state.education_debt > 0:
            self.state.education_debt += self.state.education_debt * 0.004  # 4.8% annual interest
        
        # Age the player
        if self.state.game_month % 12 == 0:
            self.state.player_age += 1
        
        # Continue or end game
        if self.state.game_month < 12:  # Play for 1 year in this demo
            continue_choice = self.get_player_input(
                "\nContinue to next month? (y/n): ", ["y", "n", "yes", "no"]
            )
            if continue_choice.lower() in ["y", "yes"]:
                self.simulate_month()
            else:
                self.end_game()
        else:
            self.end_game()
    
    def display_financial_status(self):
        """Display current financial status"""
        print(f"Age: {self.state.player_age}")
        print(f"Cash: ${self.state.cash:,.2f}")
        print(f"Monthly Income: ${self.state.monthly_income:,.2f}")
        if self.state.education_debt > 0:
            print(f"Student Debt: ${self.state.education_debt:,.2f}")
        print(f"Net Worth: ${self.state.get_net_worth():,.2f}")
        print(f"Credit Score: {self.state.credit_score}")
        print()
    
    def monthly_budgeting(self):
        """Handle monthly budgeting decisions"""
        print("TIME TO BUDGET YOUR MONEY!")
        print(f"This month you earned: ${self.state.monthly_income:,.2f}")
        print()
        
        remaining_income = self.state.monthly_income
        
        # Essential expenses
        print("First, let's handle your essential expenses:")
        
        # Housing
        if self.state.education_path in ["Four-year college", "Community college/Trade school"]:
            housing_cost = 800  # Dorm/shared apartment
            print(f"Housing (dorm/shared apartment): ${housing_cost:,.2f}")
        else:
            housing_cost = 600  # Shared living situation
            print(f"Housing (shared apartment): ${housing_cost:,.2f}")
        
        self.state.monthly_expenses["housing"] = housing_cost
        remaining_income -= housing_cost
        
        # Food
        food_cost = 300
        print(f"Food: ${food_cost:,.2f}")
        self.state.monthly_expenses["food"] = food_cost
        remaining_income -= food_cost
        
        # Transportation
        transport_choice = self.get_player_input(
            f"Transportation: (1) Public transit ($80/month) or (2) Used car ($200/month)? (1/2): ",
            ["1", "2"]
        )
        
        if transport_choice == "1":
            transport_cost = 80
            print("You chose public transportation - economical choice!")
        else:
            transport_cost = 200
            print("You chose to have a car - more expensive but convenient!")
        
        self.state.monthly_expenses["transportation"] = transport_cost
        remaining_income -= transport_cost
        
        print(f"\nRemaining income for discretionary spending: ${remaining_income:,.2f}")
        
        # Discretionary spending
        if remaining_income > 0:
            print("\nHow would you like to allocate your remaining money?")
            print("1. Entertainment/Fun")
            print("2. Savings")
            print("3. Extra debt payments (if you have debt)")
            print("4. Split between categories")
            
            choice = self.get_player_input("Choose allocation method (1-4): ", ["1", "2", "3", "4"])
            
            if choice == "1":
                self.state.monthly_expenses["entertainment"] = remaining_income
                self.state.wellbeing_score += 5
                print("You spent it all on fun! Your happiness increased but no savings.")
                
            elif choice == "2":
                self.state.monthly_expenses["savings"] = remaining_income
                self.state.savings_account += remaining_income
                print("Smart! You saved all your extra money.")
                
            elif choice == "3" and self.state.education_debt > 0:
                self.state.monthly_expenses["debt_payments"] = remaining_income
                self.state.education_debt -= remaining_income
                print("Excellent! You made extra payments on your debt.")
                
            elif choice == "4":
                entertainment = remaining_income * 0.5
                savings = remaining_income * 0.3
                debt_payment = remaining_income * 0.2
                
                self.state.monthly_expenses["entertainment"] = entertainment
                self.state.monthly_expenses["savings"] = savings
                self.state.savings_account += savings
                
                if self.state.education_debt > 0:
                    self.state.monthly_expenses["debt_payments"] = debt_payment
                    self.state.education_debt -= debt_payment
                
                print("Balanced approach! You split your money wisely.")
    
    def random_event(self):
        """Generate a random life event"""
        events = [
            {
                "name": "Car Repair",
                "description": "Your car broke down and needs $500 in repairs.",
                "cost": 500,
                "wellbeing_impact": -5
            },
            {
                "name": "Work Bonus",
                "description": "Great job! You received a $300 bonus at work.",
                "cost": -300,
                "wellbeing_impact": 10
            },
            {
                "name": "Medical Bill",
                "description": "You had to visit the doctor. Bill: $200.",
                "cost": 200,
                "wellbeing_impact": -3
            },
            {
                "name": "Tax Refund",
                "description": "You got a tax refund of $400!",
                "cost": -400,
                "wellbeing_impact": 5
            }
        ]
        
        event = random.choice(events)
        
        print(f"\n🎲 RANDOM EVENT: {event['name']}")
        print(f"   {event['description']}")
        
        self.state.cash -= event['cost']
        self.state.wellbeing_score += event['wellbeing_impact']
        
        if event['cost'] > 0:
            print(f"   This cost you ${event['cost']:,.2f}")
        else:
            print(f"   You gained ${abs(event['cost']):,.2f}")
    
    def play_random_minigame(self):
        """Play a random mini-game appropriate to player's situation"""
        game_type = get_random_minigame(self.state.cash, self.state.monthly_income)
        
        if game_type is None:
            return
        
        print(f"\n🎮 MINI-GAME OPPORTUNITY!")
        play_choice = self.get_player_input(
            "Would you like to play a quick financial mini-game? (y/n): ",
            ["y", "n", "yes", "no"]
        )
        
        if play_choice.lower() not in ["y", "yes"]:
            print("Maybe next time!")
            return
        
        result = None
        
        if game_type == "comparison_shopping":
            game = ComparisonShoppingGame()
            budget = min(self.state.cash * 0.3, 1000)  # Use up to 30% of cash or $1000
            result = game.play(budget)
            
            if result["success"]:
                self.state.cash -= result["cost"]
                self.state.wellbeing_score += result["wellbeing_bonus"]
        
        elif game_type == "budget_allocation":
            game = BudgetAllocationGame()
            result = game.play(self.state.monthly_income)
            
            if result["success"]:
                # Apply the budget allocations as a one-time adjustment
                self.state.wellbeing_score += result["wellbeing_bonus"]
                print("💡 You practiced budgeting skills!")
        
        elif game_type == "investment_simulation":
            game = InvestmentSimulationGame()
            investment_amount = min(self.state.cash * 0.2, 2000)  # Use up to 20% of cash or $2000
            
            if investment_amount < 500:
                print("You need at least $500 to play the investment game.")
                return
                
            result = game.play(investment_amount)
            
            if result["success"]:
                # For simulation purposes, just apply a small immediate benefit
                self.state.cash -= investment_amount
                self.state.investments["index_funds"] += investment_amount
                self.state.wellbeing_score += result["wellbeing_bonus"]
                print("💡 You learned about investing and started building wealth!")
        
        if result and result["success"]:
            print("\n📚 LESSON LEARNED:")
            lessons = {
                "comparison_shopping": "Always compare options before making purchases. The most expensive isn't always the best value!",
                "budget_allocation": "A good budget allocates 25-30% to housing, 20% to savings, and controls discretionary spending.",
                "investment_basics": "Investing early and consistently is one of the best ways to build long-term wealth."
            }
            print(f"   {lessons.get(result['lesson'], 'Every financial decision is a learning opportunity!')}")
    
    def save_game(self, filename: Optional[str] = None):
        """Save the current game state"""
        if filename is None:
            filename = f"{self.state.player_name}_save.json"
        
        filepath = os.path.join(self.save_directory, filename)
        
        self.state.save_date = datetime.now().isoformat()
        
        try:
            with open(filepath, 'w') as f:
                json.dump(self.state.to_dict(), f, indent=2)
            print(f"Game saved as {filename}")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self) -> bool:
        """Load a saved game"""
        save_files = [f for f in os.listdir(self.save_directory) if f.endswith('.json')]
        
        if not save_files:
            print("No saved games found.")
            return False
        
        print("\nSaved Games:")
        for i, filename in enumerate(save_files, 1):
            print(f"{i}. {filename}")
        
        try:
            choice = int(input("Choose a save file (number): ")) - 1
            if 0 <= choice < len(save_files):
                filepath = os.path.join(self.save_directory, save_files[choice])
                
                with open(filepath, 'r') as f:
                    save_data = json.load(f)
                
                self.state.from_dict(save_data)
                print(f"Game loaded: {self.state.player_name}")
                return True
            else:
                print("Invalid choice.")
                return False
        except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading game: {e}")
            return False
    
    def end_game(self):
        """End the game and show final results"""
        print("\n" + "=" * 60)
        print("GAME OVER - YOUR FINANCIAL JOURNEY SUMMARY")
        print("=" * 60)
        print()
        print(f"Player: {self.state.player_name}")
        print(f"Age: {self.state.player_age}")
        print(f"Months Played: {self.state.game_month}")
        print(f"Education Path: {self.state.education_path}")
        print()
        print("FINAL FINANCIAL STATUS:")
        print(f"Cash: ${self.state.cash:,.2f}")
        print(f"Savings: ${self.state.savings_account:,.2f}")
        if self.state.education_debt > 0:
            print(f"Student Debt: ${self.state.education_debt:,.2f}")
        print(f"Net Worth: ${self.state.get_net_worth():,.2f}")
        print(f"Credit Score: {self.state.credit_score}")
        print(f"Well-being Score: {self.state.wellbeing_score}/100")
        print()
        print("LIFE GOALS:")
        for goal in self.state.life_goals:
            status = "✓" if goal in self.state.goals_completed else "○"
            print(f"  {status} {goal}")
        print()
        
        # Offer to save
        save_choice = self.get_player_input("Save this game? (y/n): ", ["y", "n", "yes", "no"])
        if save_choice.lower() in ["y", "yes"]:
            self.save_game()
        
        print("Thanks for playing ChoiceCents!")
        self.running = False
    
    def run(self):
        """Main game loop"""
        self.display_welcome()
        
        while self.running:
            choice = self.display_main_menu()
            
            if choice == "1":
                self.new_game()
            elif choice == "2":
                if self.load_game():
                    self.simulate_month()
            elif choice == "3":
                print("Thanks for playing ChoiceCents!")
                self.running = False


if __name__ == "__main__":
    game = GameEngine()
    game.run()