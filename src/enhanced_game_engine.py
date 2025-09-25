"""
Enhanced Game Engine for ChoiceCents
Uses configuration and UI abstraction for better maintainability
"""

import json
import os
import random
from datetime import datetime
from typing import Dict, Any, List, Optional

from config import GameConfig, GameText, Achievements
from ui_interface import create_interface, UserInterface
from minigames import ComparisonShoppingGame, BudgetAllocationGame, InvestmentSimulationGame, get_random_minigame


class GameState:
    """Enhanced game state management"""
    
    def __init__(self):
        # Initialize with configuration defaults
        self.player_name: str = ""
        self.player_age: int = GameConfig.STARTING_AGE
        self.current_chapter: int = 1
        self.game_month: int = 0
        
        # Financial State
        self.cash: float = GameConfig.STARTING_CASH
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
        self.credit_score: int = GameConfig.STARTING_CREDIT_SCORE
        
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
        self.wellbeing_score: int = GameConfig.STARTING_WELLBEING
        self.goals_completed: List[str] = []
        self.achievements_earned: List[str] = []
        
        # Enhanced features for Phase 2
        self.vehicle: Optional[str] = None
        self.vehicle_condition: int = 100
        self.part_time_job: Optional[str] = None
        self.debt: float = 0.0
        self.career_started: bool = False
        
        # Game Metadata
        self.save_date: str = ""
        self.total_playtime: int = 0
        
    def get_net_worth(self) -> float:
        """Calculate total net worth"""
        assets = (self.cash + self.savings_account + 
                 sum(self.investments.values()))
        debts = self.education_debt
        return assets - debts
    
    def get_monthly_cash_flow(self) -> float:
        """Calculate monthly cash flow"""
        total_expenses = sum(self.monthly_expenses.values())
        return self.monthly_income - total_expenses
    
    def check_achievements(self) -> List[str]:
        """Check for newly earned achievements"""
        new_achievements = []
        
        for achievement_id, achievement in Achievements.ACHIEVEMENT_LIST.items():
            if achievement_id in self.achievements_earned:
                continue
                
            # Simple condition checking (could be expanded)
            condition = achievement["condition"]
            
            if condition == "monthly_income > 0" and self.monthly_income > 0:
                new_achievements.append(achievement_id)
            elif condition == "savings_account >= 1000" and self.savings_account >= 1000:
                new_achievements.append(achievement_id)
            elif condition == "education_debt <= 0" and self.education_debt <= 0:
                new_achievements.append(achievement_id)
            elif condition == "sum(investments.values()) > 0" and sum(self.investments.values()) > 0:
                new_achievements.append(achievement_id)
            elif condition == "credit_score >= 750" and self.credit_score >= 750:
                new_achievements.append(achievement_id)
            elif condition == "get_net_worth() > 0" and self.get_net_worth() > 0:
                new_achievements.append(achievement_id)
        
        # Add to earned achievements
        for achievement_id in new_achievements:
            self.achievements_earned.append(achievement_id)
            self.wellbeing_score += Achievements.ACHIEVEMENT_LIST[achievement_id]["reward_wellbeing"]
        
        return new_achievements
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for saving"""
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
            "achievements_earned": self.achievements_earned,
            "vehicle": self.vehicle,
            "vehicle_condition": self.vehicle_condition,
            "part_time_job": self.part_time_job,
            "debt": self.debt,
            "career_started": self.career_started,
            "save_date": self.save_date,
            "total_playtime": self.total_playtime
        }
    
    def from_dict(self, data: Dict[str, Any]):
        """Load from dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)


class EnhancedGameEngine:
    """Enhanced game engine with better architecture"""
    
    def __init__(self, interface_type: str = "console"):
        self.ui: UserInterface = create_interface(interface_type)
        self.state = GameState()
        self.running = True
        
        # Ensure configuration is valid
        if not GameConfig.validate_config():
            self.ui.display_text("Configuration validation failed!", "error")
            exit(1)
    
    def run(self):
        """Main game loop"""
        self.ui.display_text(GameText.WELCOME_MESSAGE)
        
        while self.running:
            choice = self.show_main_menu()
            
            if choice == "1":
                self.new_game()
            elif choice == "2":
                if self.load_game():
                    self.continue_game()
            elif choice == "3":
                self.show_about()
            elif choice == "4":
                self.ui.display_text("Thanks for playing ChoiceCents!", "success")
                self.running = False
    
    def show_main_menu(self) -> str:
        """Show main menu and get choice"""
        options = ["New Game", "Load Game", "About", "Quit"]
        return self.ui.display_menu("MAIN MENU", options)
    
    def show_about(self):
        """Show about information"""
        about_text = f"""
{GameConfig.TITLE} v{GameConfig.VERSION}

A personal finance education game designed to teach students
about budgeting, saving, investing, and financial decision-making
through interactive storytelling.

Learning Objectives:
• Budgeting and spending allocation
• Career and education planning
• Credit and debt management
• Saving and investing basics
• Long-term financial planning

This game is designed for middle and high school students
but can be educational for anyone learning about personal finance.

Press Enter to return to main menu...
"""
        self.ui.display_text(about_text)
        self.ui.pause_for_input()
    
    def new_game(self):
        """Start a new game"""
        self.ui.display_header("CHARACTER CREATION")
        
        # Get player name
        while True:
            name = self.ui.get_input("What's your name? ")
            if name.strip():
                self.state.player_name = name.strip()
                break
            self.ui.display_text("Please enter a name.", "warning")
        
        self.ui.display_text(f"\nHello, {self.state.player_name}!")
        self.ui.display_text("You're 18 years old and about to graduate high school.")
        self.ui.display_text("It's time to make some important decisions about your future!")
        
        self.select_life_goals()
        self.start_chapter_1()
    
    def select_life_goals(self):
        """Let player select life goals"""
        self.ui.display_text("\nWhat are your main life goals? (Choose up to 3)")
        
        for i, goal in enumerate(GameText.LIFE_GOALS_OPTIONS, 1):
            self.ui.display_text(f"{i}. {goal}")
        
        self.ui.display_text("\nEnter the numbers of your chosen goals (e.g., 1,3,5):")
        
        while True:
            try:
                response = self.ui.get_input("Goals: ")
                goal_nums = [int(num.strip()) for num in response.split(',') if num.strip()]
                
                if len(goal_nums) <= GameConfig.MAX_LIFE_GOALS and \
                   all(1 <= num <= len(GameText.LIFE_GOALS_OPTIONS) for num in goal_nums):
                    self.state.life_goals = [GameText.LIFE_GOALS_OPTIONS[num-1] for num in goal_nums]
                    break
                else:
                    self.ui.display_text(f"Please enter up to {GameConfig.MAX_LIFE_GOALS} valid numbers.", "warning")
            except ValueError:
                self.ui.display_text("Please enter numbers separated by commas.", "warning")
        
        self.ui.display_text(f"\nGreat! Your goals are: {', '.join(self.state.life_goals)}", "success")
        self.ui.display_text("Remember these as you make decisions - they'll guide your journey!")
        self.ui.pause_for_input()
    
    def start_chapter_1(self):
        """Chapter 1: High School Graduation"""
        self.ui.display_text(GameText.CHAPTER_1_INTRO)
        
        self.ui.display_text("Your options:")
        for key, path in GameText.EDUCATION_PATHS.items():
            self.ui.display_text(f"{key}. {path['name']} - {path['description']}")
        
        choice = self.ui.get_input("\nWhat path will you choose? (1-5): ", 
                                 list(GameText.EDUCATION_PATHS.keys()))
        
        self.process_education_choice(choice)
    
    def process_education_choice(self, choice: str):
        """Process education path choice"""
        path = GameText.EDUCATION_PATHS[choice]
        
        self.state.education_path = path["name"]
        
        if "debt" in path:
            self.state.education_debt = path["debt"]
            self.state.cash -= min(2000, self.state.cash * 0.2)  # Initial costs
        
        if "startup_cost" in path:
            self.state.cash -= path["startup_cost"]
        
        if "immediate_income" in path:
            self.state.monthly_income = path["immediate_income"]
        
        self.ui.display_text(f"\nYou've chosen: {path['name']}!", "success")
        
        # Show consequences
        if path.get("debt", 0) > 0:
            self.ui.display_text(f"This will cost about ${path['debt']:,} in loans.", "warning")
        if path.get("immediate_income", 0) > 0:
            self.ui.display_text(f"You'll start earning ${path['immediate_income']:,}/month.", "success")
        if "startup_cost" in path:
            self.ui.display_text(f"You've invested ${path['startup_cost']:,} in startup costs.", "info")
        
        self.ui.pause_for_input()
        self.continue_game()
    
    def continue_game(self):
        """Enhanced simulation with complex decision-making"""
        # Vehicle decision if player is old enough and doesn't have one
        if self.state.player_age >= 16 and not hasattr(self.state, 'vehicle'):
            self.vehicle_decision()
        
        # Part-time job consideration for students
        if self.state.education_path in ["Community college", "4-Year University", "Trade School"]:
            self.part_time_job_decision()
        
        # Enhanced monthly simulation with time scaling
        self.enhanced_monthly_simulation()
        
        self.end_game()
    
    def enhanced_monthly_simulation(self):
        """Enhanced simulation with time scaling and complex decisions"""
        current_month = 1
        target_months = GameConfig.SIMULATION_LENGTH_MONTHS  # From config (36 months)
        
        while current_month <= target_months:
            # Show current month and age
            age_in_months = (self.state.player_age * 12) + current_month
            current_age = age_in_months // 12
            self.state.player_age = current_age  # Update player age
            
            self.ui.display_header(f"MONTH {current_month} - AGE {current_age}")
            
            # Regular monthly simulation
            self.simulate_month()
            
            # Time scaling decision every few months
            if current_month % 3 == 0 and current_month < target_months:
                time_choice = self.time_scaling_decision(current_month, target_months)
                if time_choice > 1:
                    # Skip ahead with simplified simulation
                    months_to_skip = min(time_choice, target_months - current_month)
                    self.skip_time_period(months_to_skip)
                    current_month += months_to_skip
                else:
                    current_month += 1
            else:
                current_month += 1
            
            # Check for major life stage transitions
            if current_age >= 22 and not hasattr(self.state, 'career_started'):
                self.career_transition()
                self.state.career_started = True
            
            # Vehicle upgrade decision every 2 years
            if current_month % 24 == 0 and hasattr(self.state, 'vehicle'):
                self.vehicle_upgrade_decision()
    
    def time_scaling_decision(self, current_month: int, target_months: int) -> int:
        """Let player choose how much time to skip"""
        remaining_months = target_months - current_month
        
        self.ui.display_text("\n⏰ TIME MANAGEMENT", "info")
        self.ui.display_text("How would you like to proceed with time?")
        
        options = []
        if remaining_months > 0:
            options.append("Continue month by month")
        if remaining_months >= 3:
            options.append("Skip ahead 3 months (quick progress)")
        if remaining_months >= 6:
            options.append("Skip ahead 6 months (fast progress)")
        
        choice = self.ui.display_menu("Time Options", options)
        
        if choice == "1":
            return 1
        elif choice == "2" and len(options) >= 2:
            return 3
        elif choice == "3" and len(options) >= 3:
            return 6
        else:
            return 1
    
    def skip_time_period(self, months: int):
        """Simulate multiple months quickly"""
        self.ui.display_text(f"\n⏩ Skipping ahead {months} months...", "info")
        
        for month in range(months):
            # Simplified month simulation
            self.state.game_month += 1
            
            # Basic income and expenses
            net_income = self.state.monthly_income - sum(self.state.monthly_expenses.values())
            self.state.cash += net_income
            
            # Small chance of events during skip
            if random.random() < 0.1:  # 10% chance per month
                self.quick_random_event()
            
            # Part-time job income if applicable
            if hasattr(self.state, 'part_time_job') and self.state.part_time_job:
                part_time_income = GameConfig.PART_TIME_JOB_WAGES.get(self.state.part_time_job, 0)
                self.state.cash += part_time_income
        
        # Show summary of skip period
        self.ui.display_text(f"📊 Summary of {months} months:", "info")
        self.ui.display_text(f"   Current cash: ${self.state.cash:,.2f}")
        if hasattr(self.state, 'vehicle'):
            self.ui.display_text(f"   Vehicle condition: {self.get_vehicle_condition()}")
        self.ui.pause_for_input()
    
    def vehicle_decision(self):
        """Let player choose a vehicle"""
        self.ui.display_header("VEHICLE DECISION")
        self.ui.display_text("You need to decide about transportation.")
        self.ui.display_text("Having a car gives you more job opportunities but costs money.")
        
        # Show vehicle options based on player's cash
        affordable_vehicles = []
        for vehicle_id, vehicle in GameConfig.VEHICLE_OPTIONS.items():
            if vehicle['purchase_cost'] <= self.state.cash * 1.2:  # Allow slight stretching
                affordable_vehicles.append((vehicle_id, vehicle))
        
        options = ["No vehicle (walk/bike/public transport)"]
        for vehicle_id, vehicle in affordable_vehicles:
            cost_text = f"${vehicle['purchase_cost']:,}"
            monthly_text = f"${vehicle['monthly_cost']:,}/month"
            options.append(f"{vehicle['name']} - {cost_text} ({monthly_text})")
        
        choice = self.ui.display_menu("Transportation Options", options)
        
        if choice == "1":
            self.state.vehicle = None
            self.ui.display_text("You decided to rely on alternative transportation.", "info")
        else:
            vehicle_index = int(choice) - 2
            if 0 <= vehicle_index < len(affordable_vehicles):
                vehicle_id, vehicle = affordable_vehicles[vehicle_index]
                
                if vehicle['purchase_cost'] > self.state.cash:
                    self.ui.display_text("You'll need to take a loan for this vehicle.", "warning")
                    loan_amount = vehicle['purchase_cost'] - self.state.cash
                    self.state.cash = 0
                    self.state.debt = getattr(self.state, 'debt', 0) + loan_amount
                else:
                    self.state.cash -= vehicle['purchase_cost']
                
                self.state.vehicle = vehicle_id
                self.state.vehicle_condition = 100  # Start with perfect condition
                self.state.monthly_expenses['transportation'] += vehicle['monthly_cost']
                
                self.ui.display_text(f"You bought a {vehicle['name']}!", "success")
                self.ui.display_text(f"Monthly costs: ${vehicle['monthly_cost']:,}", "info")
        
        self.ui.pause_for_input()
    
    def part_time_job_decision(self):
        """Let student decide about part-time work"""
        self.ui.display_header("PART-TIME JOB OPPORTUNITY")
        self.ui.display_text("As a student, you can work part-time to earn extra money.")
        self.ui.display_text("However, working too much might affect your grades!")
        
        # Show available part-time jobs
        available_jobs = []
        for job_id, job_info in GameConfig.PART_TIME_JOBS.items():
            education_req = job_info.get('education_compatible', [])
            if not education_req or self.state.education_path in education_req:
                available_jobs.append((job_id, job_info))
        
        options = ["Focus only on studies (no part-time job)"]
        for job_id, job_info in available_jobs:
            wage_text = f"${job_info['hourly_wage']}/hour"
            hours_text = f"~{job_info['max_hours_per_week']} hours/week"
            options.append(f"{job_info['title']} - {wage_text} ({hours_text})")
        
        choice = self.ui.display_menu("Part-time Job Options", options)
        
        if choice == "1":
            self.state.part_time_job = None
            self.ui.display_text("You decided to focus entirely on your studies.", "info")
        else:
            job_index = int(choice) - 2
            if 0 <= job_index < len(available_jobs):
                job_id, job_info = available_jobs[job_index]
                self.state.part_time_job = job_id
                
                # Calculate monthly income (assuming 4 weeks per month)
                weekly_income = job_info['hourly_wage'] * job_info['max_hours_per_week']
                monthly_income = weekly_income * 4
                
                self.state.monthly_income += monthly_income
                self.ui.display_text(f"You got a job as a {job_info['title']}!", "success")
                self.ui.display_text(f"Additional monthly income: ${monthly_income:,}", "success")
                
                # Slight impact on wellbeing due to busy schedule
                self.state.wellbeing_score -= 5
                self.ui.display_text("Your schedule is busier now, affecting your free time.", "warning")
        
        self.ui.pause_for_input()
    
    def get_vehicle_condition(self) -> str:
        """Get vehicle condition description"""
        if not hasattr(self.state, 'vehicle') or not self.state.vehicle:
            return "No vehicle"
        
        condition = self.state.vehicle_condition
        if condition >= 90:
            return "Excellent"
        elif condition >= 75:
            return "Good"
        elif condition >= 50:
            return "Fair"
        elif condition >= 25:
            return "Poor"
        else:
            return "Very Poor"
    
    def quick_random_event(self):
        """Simplified random event for time skips"""
        events = [
            {"name": "Minor expense", "cost": random.randint(50, 200)},
            {"name": "Small windfall", "cost": -random.randint(100, 300)},
            {"name": "Vehicle maintenance", "cost": random.randint(100, 400), "requires_vehicle": True}
        ]
        
        available_events = []
        for event in events:
            if event.get("requires_vehicle") and not hasattr(self.state, 'vehicle'):
                continue
            available_events.append(event)
        
        if available_events:
            event = random.choice(available_events)
            self.state.cash -= event['cost']
    
    def career_transition(self):
        """Handle transition from education to career"""
        self.ui.display_header("CAREER TRANSITION")
        self.ui.display_text("You're ready to start your career!", "success")
        
        # Load expanded career data
        try:
            with open('data/expanded_content.json', 'r') as f:
                career_data = json.load(f)
        except FileNotFoundError:
            self.ui.display_text("Career data not found, using basic options.", "warning")
            return
        
        # Select appropriate career options based on education
        education_to_career = {
            "High School": "high_school_entry",
            "Community College": "associate_degree", 
            "Trade School": "trade_school",
            "4-Year University": "bachelor_degree",
            "Military Service": "military_specializations"
        }
        
        career_category = education_to_career.get(self.state.education_path, "high_school_entry")
        available_careers = career_data.get("expanded_careers", {}).get(career_category, [])
        
        if available_careers:
            options = []
            for career in available_careers[:5]:  # Show top 5 options
                options.append(f"{career['title']} - Starting: ${career['starting_salary']:,}/year")
            
            choice = self.ui.display_menu("Career Options", options)
            selected_career = available_careers[int(choice) - 1]
            
            self.state.career = selected_career['title']
            self.state.monthly_income = selected_career['starting_salary'] / 12
            
            self.ui.display_text(f"Congratulations! You're now a {selected_career['title']}!", "success")
            self.ui.display_text(f"Starting salary: ${selected_career['starting_salary']:,}/year", "info")
            
            # Remove part-time job if transitioning to full-time career
            if hasattr(self.state, 'part_time_job') and self.state.part_time_job:
                self.state.part_time_job = None
                self.ui.display_text("You've left your part-time job for your career.", "info")
    
    def vehicle_upgrade_decision(self):
        """Let player decide whether to upgrade their vehicle"""
        if not hasattr(self.state, 'vehicle') or not self.state.vehicle:
            return
        
        current_vehicle = GameConfig.VEHICLE_OPTIONS.get(self.state.vehicle)
        if not current_vehicle:
            return
        
        self.ui.display_header("VEHICLE DECISION")
        self.ui.display_text(f"Your {current_vehicle['name']} is getting older.")
        self.ui.display_text(f"Current condition: {self.get_vehicle_condition()}")
        
        # Vehicle condition decreases over time
        self.state.vehicle_condition -= random.randint(5, 15)
        
        if self.state.vehicle_condition < 50:
            self.ui.display_text("Your vehicle is becoming unreliable and may need replacement soon.", "warning")
        
        options = [
            "Keep current vehicle",
            "Upgrade to a newer vehicle",
            "Sell vehicle and go without"
        ]
        
        choice = self.ui.display_menu("Vehicle Options", options)
        
        if choice == "2":  # Upgrade
            self.vehicle_decision()  # Reuse vehicle selection logic
        elif choice == "3":  # Sell
            sale_value = max(1000, current_vehicle['purchase_cost'] * 0.3)  # Depreciated value
            self.state.cash += sale_value
            self.state.vehicle = None
            self.state.monthly_expenses['transportation'] -= current_vehicle['monthly_cost']
            self.ui.display_text(f"You sold your vehicle for ${sale_value:,}", "success")
    
    def simulate_month(self):
        """Simulate one month"""
        self.state.game_month += 1
        
        self.ui.display_header(f"MONTH {self.state.game_month}")
        
        # Display financial status
        status = {
            'age': self.state.player_age,
            'month': self.state.game_month,
            'cash': self.state.cash,
            'monthly_income': self.state.monthly_income,
            'education_debt': self.state.education_debt,
            'savings_account': self.state.savings_account,
            'net_worth': self.state.get_net_worth(),
            'credit_score': self.state.credit_score,
            'wellbeing_score': self.state.wellbeing_score
        }
        self.ui.display_financial_status(status)
        
        # Monthly budgeting if player has income
        if self.state.monthly_income > 0:
            self.monthly_budgeting()
        
        # Random events
        if random.random() < GameConfig.RANDOM_EVENT_CHANCE:
            self.random_event()
        
        # Mini-games
        if random.random() < GameConfig.MINIGAME_CHANCE:
            self.play_random_minigame()
        
        # Apply monthly changes
        self.apply_monthly_changes()
        
        # Check achievements
        new_achievements = self.state.check_achievements()
        for achievement_id in new_achievements:
            achievement = Achievements.ACHIEVEMENT_LIST[achievement_id]
            self.ui.display_text(f"🏆 ACHIEVEMENT UNLOCKED: {achievement['name']}", "success")
            self.ui.display_text(f"   {achievement['description']}")
    
    def monthly_budgeting(self):
        """Handle monthly budgeting"""
        self.ui.display_text(f"\n💰 MONTHLY BUDGETING")
        self.ui.display_text(f"Income this month: ${self.state.monthly_income:,.2f}")
        
        # Essential expenses
        housing_cost = GameConfig.LIVING_COSTS["housing_student"] if "college" in self.state.education_path.lower() else GameConfig.LIVING_COSTS["housing_shared"]
        food_cost = GameConfig.LIVING_COSTS["food_basic"]
        
        self.ui.display_text(f"\nEssential expenses:")
        self.ui.display_text(f"Housing: ${housing_cost:,.2f}")
        self.ui.display_text(f"Food: ${food_cost:,.2f}")
        
        # Transportation choice
        transport_choice = self.ui.get_input(
            f"Transportation: (1) Public transit (${GameConfig.LIVING_COSTS['transport_public']}/month) or (2) Car (${GameConfig.LIVING_COSTS['transport_car']}/month)? (1/2): ",
            ["1", "2"]
        )
        
        transport_cost = GameConfig.LIVING_COSTS["transport_public"] if transport_choice == "1" else GameConfig.LIVING_COSTS["transport_car"]
        
        # Update expenses
        self.state.monthly_expenses["housing"] = housing_cost
        self.state.monthly_expenses["food"] = food_cost
        self.state.monthly_expenses["transportation"] = transport_cost
        
        remaining = self.state.monthly_income - housing_cost - food_cost - transport_cost
        
        self.ui.display_text(f"\nRemaining for discretionary spending: ${remaining:,.2f}")
        
        if remaining > 0:
            self.allocate_discretionary_spending(remaining)
    
    def allocate_discretionary_spending(self, remaining: float):
        """Handle discretionary spending allocation"""
        options = ["Entertainment/Fun", "Savings", "Extra debt payments", "Split between categories"]
        choice = self.ui.display_menu("How to allocate remaining money?", options)
        
        if choice == "1":  # Entertainment
            self.state.monthly_expenses["entertainment"] = remaining
            self.state.wellbeing_score += 5
            self.ui.display_text("You spent it all on fun! Happiness increased.", "info")
        
        elif choice == "2":  # Savings
            self.state.monthly_expenses["savings"] = remaining
            self.state.savings_account += remaining
            self.ui.display_text("Smart! You saved all your extra money.", "success")
        
        elif choice == "3" and self.state.education_debt > 0:  # Debt payments
            self.state.monthly_expenses["debt_payments"] = remaining
            self.state.education_debt -= remaining
            self.ui.display_text("Excellent! You made extra debt payments.", "success")
        
        elif choice == "4":  # Split
            entertainment = remaining * 0.5
            savings = remaining * 0.3
            debt_payment = remaining * 0.2
            
            self.state.monthly_expenses["entertainment"] = entertainment
            self.state.monthly_expenses["savings"] = savings
            self.state.savings_account += savings
            self.state.wellbeing_score += 3
            
            if self.state.education_debt > 0:
                self.state.monthly_expenses["debt_payments"] = debt_payment
                self.state.education_debt -= debt_payment
            
            self.ui.display_text("Balanced approach! You split your money wisely.", "success")
    
    def random_event(self):
        """Generate random life event using expanded content"""
        # Try to load expanded events
        try:
            with open('data/expanded_content.json', 'r') as f:
                content_data = json.load(f)
            
            # Choose event type based on probability
            event_roll = random.random()
            if event_roll < 0.4:  # 40% chance positive
                event_pool = content_data.get("life_events", {}).get("positive_events", [])
            elif event_roll < 0.8:  # 40% chance negative  
                event_pool = content_data.get("life_events", {}).get("negative_events", [])
            else:  # 20% chance neutral
                event_pool = content_data.get("life_events", {}).get("neutral_events", [])
            
            # Filter events based on conditions
            available_events = []
            for event in event_pool:
                conditions = event.get("conditions", [])
                if self.check_event_conditions(conditions):
                    available_events.append(event)
            
            if available_events:
                event = random.choice(available_events)
                self.process_expanded_event(event)
                return
                
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass  # Fall back to basic events
        
        # Basic fallback events
        basic_events = [
            {"name": "Car Repair", "description": "Your car needs $500 in repairs.", "cost": 500, "wellbeing": -5},
            {"name": "Work Bonus", "description": "Great job! You got a $300 bonus.", "cost": -300, "wellbeing": 10},
            {"name": "Medical Bill", "description": "Doctor visit cost $200.", "cost": 200, "wellbeing": -3},
            {"name": "Tax Refund", "description": "You got a $400 tax refund!", "cost": -400, "wellbeing": 5}
        ]
        
        event = random.choice(basic_events)
        
        self.ui.display_text(f"\n🎲 RANDOM EVENT: {event['name']}", "info")
        self.ui.display_text(f"   {event['description']}")
        
        self.state.cash -= event['cost']
        self.state.wellbeing_score += event['wellbeing']
        
        if event['cost'] > 0:
            self.ui.display_text(f"   Cost: ${event['cost']:,.2f}", "warning")
        else:
            self.ui.display_text(f"   Gained: ${abs(event['cost']):,.2f}", "success")
    
    def check_event_conditions(self, conditions: List[str]) -> bool:
        """Check if player meets event conditions"""
        for condition in conditions:
            if condition == "has_income" and self.state.monthly_income <= 0:
                return False
            elif condition == "owns_car" and not hasattr(self.state, 'vehicle'):
                return False
            elif condition == "has_job" and not self.state.career and not hasattr(self.state, 'part_time_job'):
                return False
            elif condition == "is_student" and self.state.education_path not in ["Community College", "4-Year University", "Trade School"]:
                return False
            elif condition == "has_credit_card" and self.state.credit_score < 500:
                return False
            elif condition == "rents_apartment" and self.state.monthly_expenses.get("housing", 0) > 0:
                return False
        return True
    
    def process_expanded_event(self, event: Dict):
        """Process an expanded event with complex effects"""
        self.ui.display_text(f"\n🎲 RANDOM EVENT: {event['name']}", "info")
        self.ui.display_text(f"   {event['description']}")
        
        # Handle cash impact
        if "cash_impact" in event:
            impact_range = event["cash_impact"]
            min_val, max_val = min(impact_range), max(impact_range)
            cash_change = random.randint(min_val, max_val)
            self.state.cash -= cash_change
            
            if cash_change > 0:
                self.ui.display_text(f"   Cost: ${cash_change:,.2f}", "warning")
            else:
                self.ui.display_text(f"   Gained: ${abs(cash_change):,.2f}", "success")
        
        # Handle wellbeing impact
        if "wellbeing_impact" in event:
            wellbeing_range = event["wellbeing_impact"]
            min_val, max_val = min(wellbeing_range), max(wellbeing_range)
            wellbeing_change = random.randint(min_val, max_val)
            self.state.wellbeing_score += wellbeing_change
            
            if wellbeing_change > 0:
                self.ui.display_text(f"   Wellbeing improved by {wellbeing_change}", "success")
            else:
                self.ui.display_text(f"   Wellbeing decreased by {abs(wellbeing_change)}", "warning")
        
        # Handle special effects
        if "debt_reduction" in event:
            reduction_range = event["debt_reduction"]
            reduction = random.randint(reduction_range[0], reduction_range[1])
            if self.state.education_debt > 0:
                actual_reduction = min(reduction, self.state.education_debt)
                self.state.education_debt -= actual_reduction
                self.ui.display_text(f"   Student loan reduced by ${actual_reduction:,.2f}!", "success")
        
        if "salary_increase" in event:
            increase_range = event["salary_increase"]
            increase_percent = random.uniform(increase_range[0], increase_range[1])
            old_income = self.state.monthly_income
            self.state.monthly_income *= (1 + increase_percent)
            increase_amount = self.state.monthly_income - old_income
            self.ui.display_text(f"   Monthly income increased by ${increase_amount:,.2f}!", "success")
        
        if "credit_score_impact" in event:
            impact_range = event["credit_score_impact"]
            score_change = random.randint(impact_range[0], impact_range[1])
            self.state.credit_score += score_change
            self.state.credit_score = max(300, min(850, self.state.credit_score))  # Keep in valid range
    
    def play_random_minigame(self):
        """Play a random mini-game"""
        game_type = get_random_minigame(self.state.cash, self.state.monthly_income)
        
        if game_type is None:
            return
        
        self.ui.display_text("\n🎮 MINI-GAME OPPORTUNITY!", "info")
        play_choice = self.ui.get_input("Play a financial mini-game? (y/n): ", ["y", "n", "yes", "no"])
        
        if play_choice.lower() not in ["y", "yes"]:
            return
        
        # Play the appropriate mini-game
        if game_type == "comparison_shopping":
            game = ComparisonShoppingGame()
            budget = min(self.state.cash * 0.3, 1000)
            result = game.play(budget)
            if result["success"]:
                self.state.cash -= result["cost"]
                self.state.wellbeing_score += result["wellbeing_bonus"]
        
        # Add other mini-games as implemented...
    
    def apply_monthly_changes(self):
        """Apply end-of-month changes"""
        # Apply cash flow
        cash_flow = self.state.get_monthly_cash_flow()
        self.state.cash += cash_flow
        
        # Apply debt interest
        if self.state.education_debt > 0:
            monthly_interest = GameConfig.DEBT_INTEREST_RATE / 12
            self.state.education_debt += self.state.education_debt * monthly_interest
        
        # Age the player
        if self.state.game_month % 12 == 0:
            self.state.player_age += 1
        
        # Ensure values stay in valid ranges
        self.state.credit_score = max(GameConfig.CREDIT_SCORE_RANGE[0], 
                                    min(self.state.credit_score, GameConfig.CREDIT_SCORE_RANGE[1]))
        self.state.wellbeing_score = max(GameConfig.WELLBEING_RANGE[0],
                                       min(self.state.wellbeing_score, GameConfig.WELLBEING_RANGE[1]))
    
    def save_game(self, filename: Optional[str] = None) -> bool:
        """Save game state"""
        if filename is None:
            filename = f"{self.state.player_name}_save.json"
        
        filepath = GameConfig.get_save_file_path(filename)
        self.state.save_date = datetime.now().isoformat()
        
        try:
            with open(filepath, 'w') as f:
                json.dump(self.state.to_dict(), f, indent=2)
            self.ui.display_text(f"Game saved as {filename}", "success")
            return True
        except Exception as e:
            self.ui.display_text(f"Error saving game: {e}", "error")
            return False
    
    def load_game(self) -> bool:
        """Load a saved game"""
        save_files = [f for f in os.listdir(GameConfig.SAVES_DIR) if f.endswith('.json')]
        
        if not save_files:
            self.ui.display_text("No saved games found.", "warning")
            return False
        
        self.ui.display_text("\nSaved Games:")
        for i, filename in enumerate(save_files, 1):
            self.ui.display_text(f"{i}. {filename}")
        
        try:
            choice_str = self.ui.get_input("Choose save file number: ")
            choice = int(choice_str) - 1
            
            if 0 <= choice < len(save_files):
                filepath = GameConfig.get_save_file_path(save_files[choice])
                
                with open(filepath, 'r') as f:
                    save_data = json.load(f)
                
                self.state.from_dict(save_data)
                self.ui.display_text(f"Game loaded: {self.state.player_name}", "success")
                return True
            else:
                self.ui.display_text("Invalid choice.", "warning")
                return False
        except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
            self.ui.display_text(f"Error loading game: {e}", "error")
            return False
    
    def end_game(self):
        """End game and show summary"""
        self.ui.display_header("GAME SUMMARY")
        
        self.ui.display_text(f"Player: {self.state.player_name}")
        self.ui.display_text(f"Age: {self.state.player_age}")
        self.ui.display_text(f"Months Played: {self.state.game_month}")
        self.ui.display_text(f"Education Path: {self.state.education_path}")
        
        self.ui.display_text("\nFINAL FINANCIAL STATUS:", "bold")
        status = {
            'age': self.state.player_age,
            'month': self.state.game_month,
            'cash': self.state.cash,
            'monthly_income': self.state.monthly_income,
            'education_debt': self.state.education_debt,
            'savings_account': self.state.savings_account,
            'net_worth': self.state.get_net_worth(),
            'credit_score': self.state.credit_score,
            'wellbeing_score': self.state.wellbeing_score
        }
        self.ui.display_financial_status(status)
        
        # Show achievements
        if self.state.achievements_earned:
            self.ui.display_text("ACHIEVEMENTS EARNED:", "success")
            for achievement_id in self.state.achievements_earned:
                achievement = Achievements.ACHIEVEMENT_LIST[achievement_id]
                self.ui.display_text(f"🏆 {achievement['name']}")
        
        # Save option
        save_choice = self.ui.get_input("Save this game? (y/n): ", ["y", "n", "yes", "no"])
        if save_choice.lower() in ["y", "yes"]:
            self.save_game()
        
        self.ui.display_text("Thanks for playing ChoiceCents!", "success")
        self.running = False


if __name__ == "__main__":
    game = EnhancedGameEngine()
    game.run()