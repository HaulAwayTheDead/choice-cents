"""
Mini-games for ChoiceCents
Educational mini-games to teach specific financial concepts
"""

import random
from typing import Dict, List, Tuple, Optional

class ComparisonShoppingGame:
    """Mini-game for teaching comparison shopping skills"""
    
    def __init__(self):
        self.products = {
            "laptop": [
                {"name": "Budget Laptop", "price": 400, "quality": 6, "warranty": 1},
                {"name": "Mid-range Laptop", "price": 700, "quality": 8, "warranty": 2},
                {"name": "Premium Laptop", "price": 1200, "quality": 9, "warranty": 3},
            ],
            "phone": [
                {"name": "Basic Phone", "price": 200, "quality": 5, "warranty": 1},
                {"name": "Popular Phone", "price": 600, "quality": 8, "warranty": 2},
                {"name": "Flagship Phone", "price": 1000, "quality": 9, "warranty": 2},
            ],
            "car": [
                {"name": "Used Compact Car", "price": 8000, "quality": 6, "mpg": 35},
                {"name": "Certified Pre-owned", "price": 15000, "quality": 8, "mpg": 30},
                {"name": "New Car", "price": 25000, "quality": 9, "mpg": 32},
            ]
        }
    
    def play(self, budget: float, category: Optional[str] = None) -> Dict:
        """Play the comparison shopping mini-game"""
        if category is None:
            category = random.choice(list(self.products.keys()))
        
        print(f"\n🛍️  COMPARISON SHOPPING MINI-GAME")
        print(f"Category: {category.title()}")
        print(f"Your budget: ${budget:,.2f}")
        print("=" * 50)
        
        products = self.products[category]
        affordable_products = [p for p in products if p["price"] <= budget]
        
        if not affordable_products:
            print("Unfortunately, none of these options fit your budget.")
            print("This teaches us the importance of saving for larger purchases!")
            return {"success": False, "lesson": "budget_constraint"}
        
        print("Available options:")
        for i, product in enumerate(affordable_products, 1):
            print(f"{i}. {product['name']}")
            print(f"   Price: ${product['price']:,}")
            print(f"   Quality Rating: {product['quality']}/10")
            if 'warranty' in product:
                print(f"   Warranty: {product['warranty']} year(s)")
            if 'mpg' in product:
                print(f"   MPG: {product['mpg']}")
            print()
        
        print("Consider:")
        print("- Which offers the best value for your needs?")
        print("- Is the most expensive always the best choice?")
        print("- How long do you plan to use this item?")
        print()
        
        while True:
            try:
                choice = int(input(f"Which would you choose? (1-{len(affordable_products)}): ")) - 1
                if 0 <= choice < len(affordable_products):
                    break
                else:
                    print("Please enter a valid option number.")
            except ValueError:
                print("Please enter a number.")
        
        chosen_product = affordable_products[choice]
        
        # Calculate value score (quality per dollar)
        value_score = chosen_product["quality"] / (chosen_product["price"] / 1000)
        
        print(f"\nYou chose: {chosen_product['name']}")
        print(f"Cost: ${chosen_product['price']:,}")
        print(f"Money remaining: ${budget - chosen_product['price']:,.2f}")
        
        # Provide feedback
        if value_score > 0.008:  # High value threshold
            print("💡 Excellent choice! You found great value for your money.")
            wellbeing_bonus = 5
        elif value_score > 0.006:  # Medium value
            print("💡 Good choice! You balanced cost and quality well.")
            wellbeing_bonus = 3
        else:
            print("💡 You chose the premium option. Sometimes quality is worth paying for!")
            wellbeing_bonus = 1
        
        return {
            "success": True,
            "cost": chosen_product["price"],
            "wellbeing_bonus": wellbeing_bonus,
            "lesson": "comparison_shopping"
        }


class BudgetAllocationGame:
    """Mini-game for teaching budget allocation skills"""
    
    def play(self, monthly_income: float) -> Dict:
        """Play the budget allocation mini-game"""
        print(f"\n💰 BUDGET ALLOCATION CHALLENGE")
        print(f"Monthly Income: ${monthly_income:,.2f}")
        print("=" * 50)
        
        print("You need to allocate your monthly income across these categories:")
        print("1. Housing (rent/mortgage) - typically 25-30% of income")
        print("2. Food (groceries/dining) - typically 10-15% of income")
        print("3. Transportation - typically 10-15% of income")
        print("4. Savings - experts recommend 20% of income")
        print("5. Entertainment/Personal - remaining amount")
        print()
        
        categories = ["Housing", "Food", "Transportation", "Savings", "Entertainment"]
        allocations = {}
        remaining = monthly_income
        
        for category in categories[:-1]:  # All except entertainment
            while True:
                try:
                    if category == "Entertainment":
                        amount = remaining
                        print(f"{category}: ${amount:,.2f} (remaining)")
                    else:
                        amount = float(input(f"How much for {category}? $"))
                    
                    if amount < 0:
                        print("Amount cannot be negative.")
                        continue
                    if amount > remaining:
                        print(f"You only have ${remaining:,.2f} remaining.")
                        continue
                    
                    allocations[category] = amount
                    remaining -= amount
                    print(f"Remaining: ${remaining:,.2f}")
                    break
                    
                except ValueError:
                    print("Please enter a valid number.")
        
        # Allocate remaining to entertainment
        allocations["Entertainment"] = remaining
        
        print(f"\nYour Budget Allocation:")
        print("=" * 30)
        total_check = 0
        for category, amount in allocations.items():
            percentage = (amount / monthly_income) * 100
            print(f"{category}: ${amount:,.2f} ({percentage:.1f}%)")
            total_check += amount
        
        print(f"Total: ${total_check:,.2f}")
        
        # Provide feedback based on recommended percentages
        feedback_score = 0
        feedback_messages = []
        
        # Housing check (25-30% is ideal)
        housing_pct = (allocations["Housing"] / monthly_income) * 100
        if 25 <= housing_pct <= 30:
            feedback_score += 20
            feedback_messages.append("✓ Housing allocation is in the ideal range!")
        elif housing_pct > 30:
            feedback_messages.append("⚠ Housing costs are high - consider a less expensive option.")
        else:
            feedback_messages.append("✓ Low housing costs give you more flexibility!")
        
        # Savings check (20% is ideal)
        savings_pct = (allocations["Savings"] / monthly_income) * 100
        if savings_pct >= 20:
            feedback_score += 25
            feedback_messages.append("✓ Excellent savings rate! You're building wealth.")
        elif savings_pct >= 10:
            feedback_score += 15
            feedback_messages.append("✓ Good start on savings - try to increase when possible.")
        else:
            feedback_messages.append("⚠ Try to save more - even 10% makes a big difference!")
        
        # Food check (10-15% is typical)
        food_pct = (allocations["Food"] / monthly_income) * 100
        if 10 <= food_pct <= 15:
            feedback_score += 15
            feedback_messages.append("✓ Food budget looks reasonable.")
        elif food_pct > 15:
            feedback_messages.append("⚠ Food costs are high - consider cooking more at home.")
        
        print(f"\nBudget Feedback:")
        for message in feedback_messages:
            print(f"  {message}")
        
        if feedback_score >= 50:
            result = "excellent"
            wellbeing_bonus = 10
        elif feedback_score >= 30:
            result = "good"  
            wellbeing_bonus = 5
        else:
            result = "needs_improvement"
            wellbeing_bonus = 2
        
        return {
            "success": True,
            "allocations": allocations,
            "feedback_score": feedback_score,
            "result": result,
            "wellbeing_bonus": wellbeing_bonus,
            "lesson": "budget_allocation"
        }


class InvestmentSimulationGame:
    """Mini-game for teaching basic investment concepts"""
    
    def __init__(self):
        self.investment_options = {
            "savings": {"name": "Savings Account", "return": 0.015, "risk": 0.001},
            "bonds": {"name": "Government Bonds", "return": 0.035, "risk": 0.005},
            "index": {"name": "Index Funds", "return": 0.07, "risk": 0.15},
            "stocks": {"name": "Individual Stocks", "return": 0.08, "risk": 0.25},
        }
    
    def play(self, investment_amount: float) -> Dict:
        """Play the investment simulation mini-game"""
        print(f"\n📈 INVESTMENT SIMULATION")
        print(f"Amount to invest: ${investment_amount:,.2f}")
        print("=" * 50)
        
        print("Investment Options (10-year simulation):")
        for key, option in self.investment_options.items():
            expected_return = investment_amount * (1 + option["return"]) ** 10
            print(f"{len(self.investment_options) - list(self.investment_options.keys()).index(key)}. {option['name']}")
            print(f"   Expected annual return: {option['return']*100:.1f}%")
            print(f"   Risk level: {'Low' if option['risk'] < 0.1 else 'Medium' if option['risk'] < 0.2 else 'High'}")
            print(f"   Expected value after 10 years: ${expected_return:,.2f}")
            print()
        
        print("Remember:")
        print("- Higher returns usually mean higher risk")
        print("- Diversification reduces risk")
        print("- Time in the market beats timing the market")
        print()
        
        while True:
            try:
                choice = int(input("Which investment would you choose? (1-4): ")) - 1
                if 0 <= choice < len(self.investment_options):
                    break
                else:
                    print("Please enter 1, 2, 3, or 4.")
            except ValueError:
                print("Please enter a number.")
        
        chosen_key = list(self.investment_options.keys())[choice]
        chosen_option = self.investment_options[chosen_key]
        
        # Simulate 10 years with random variations
        final_amount = investment_amount
        years_data = []
        
        for year in range(1, 11):
            # Add randomness based on risk level
            random_factor = random.gauss(1, chosen_option["risk"])
            annual_return = chosen_option["return"] * random_factor
            final_amount *= (1 + annual_return)
            years_data.append((year, final_amount, annual_return))
        
        print(f"\nYou chose: {chosen_option['name']}")
        print(f"10-Year Investment Simulation Results:")
        print("Year | Value     | Annual Return")
        print("-" * 35)
        
        for year, value, return_rate in years_data[-5:]:  # Show last 5 years
            print(f"{year:4d} | ${value:8,.0f} | {return_rate:8.1%}")
        
        total_return = final_amount - investment_amount
        total_return_pct = (final_amount / investment_amount - 1) * 100
        
        print("-" * 35)
        print(f"Final Value: ${final_amount:,.2f}")
        print(f"Total Return: ${total_return:,.2f} ({total_return_pct:.1f}%)")
        
        # Provide educational feedback
        if chosen_key == "savings":
            lesson = "Safe choice! Low risk means steady, predictable growth."
        elif chosen_key == "bonds":
            lesson = "Conservative approach with slightly better returns than savings."
        elif chosen_key == "index":
            lesson = "Excellent choice! Index funds offer good diversification and long-term growth."
        else:  # stocks
            lesson = "High risk, high reward! Individual stocks can be volatile but offer great potential."
        
        print(f"\n💡 {lesson}")
        
        return {
            "success": True,
            "final_amount": final_amount,
            "total_return": total_return,
            "investment_type": chosen_option["name"],
            "lesson": "investment_basics",
            "wellbeing_bonus": 3
        }


def get_random_minigame(player_cash: float, monthly_income: float) -> Optional[str]:
    """Select an appropriate mini-game based on player's financial situation"""
    games = []
    
    if player_cash >= 500:
        games.append("comparison_shopping")
    
    if monthly_income > 0:
        games.append("budget_allocation")
    
    if player_cash >= 1000:
        games.append("investment_simulation")
    
    return random.choice(games) if games else None