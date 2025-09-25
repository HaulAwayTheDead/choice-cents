"""
User Interface Abstraction Layer for ChoiceCents
This module provides an abstraction layer that can be easily swapped
between console interface and GUI interface in the future.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Union
import sys

class UserInterface(ABC):
    """Abstract base class for user interfaces"""
    
    @abstractmethod
    def display_text(self, text: str, style: str = "normal"):
        """Display text to the user"""
        pass
    
    @abstractmethod
    def display_header(self, text: str):
        """Display a header/title"""
        pass
    
    @abstractmethod
    def display_separator(self, length: int = 50):
        """Display a separator line"""
        pass
    
    @abstractmethod
    def get_input(self, prompt: str, valid_options: Optional[List[str]] = None) -> str:
        """Get input from user with optional validation"""
        pass
    
    @abstractmethod
    def get_number_input(self, prompt: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> float:
        """Get numeric input from user"""
        pass
    
    @abstractmethod
    def display_menu(self, title: str, options: List[str]) -> str:
        """Display a menu and get user selection"""
        pass
    
    @abstractmethod
    def display_financial_status(self, status: Dict[str, Any]):
        """Display financial status information"""
        pass
    
    @abstractmethod
    def display_progress_bar(self, current: int, total: int, label: str = ""):
        """Display a progress indicator"""
        pass
    
    @abstractmethod
    def clear_screen(self):
        """Clear the display"""
        pass
    
    @abstractmethod
    def pause_for_input(self, message: str = "Press Enter to continue..."):
        """Pause and wait for user acknowledgment"""
        pass


class ConsoleInterface(UserInterface):
    """Console-based user interface implementation"""
    
    def __init__(self):
        self.width = 60
    
    def display_text(self, text: str, style: str = "normal"):
        """Display text to console with optional styling"""
        if style == "bold":
            print(f"\033[1m{text}\033[0m")
        elif style == "success":
            print(f"\033[92m{text}\033[0m")  # Green
        elif style == "warning":
            print(f"\033[93m{text}\033[0m")  # Yellow
        elif style == "error":
            print(f"\033[91m{text}\033[0m")  # Red
        elif style == "info":
            print(f"\033[94m{text}\033[0m")  # Blue
        else:
            print(text)
    
    def display_header(self, text: str):
        """Display a formatted header"""
        self.display_separator()
        self.display_text(f"  {text}", "bold")
        self.display_separator()
    
    def display_separator(self, length: Optional[int] = None):
        """Display a separator line"""
        if length is None:
            length = self.width
        print("=" * length)
    
    def get_input(self, prompt: str, valid_options: Optional[List[str]] = None) -> str:
        """Get validated input from user"""
        while True:
            try:
                response = input(prompt).strip()
                
                if valid_options is None:
                    return response
                
                # Check if response matches any valid option (case-insensitive)
                response_lower = response.lower()
                for option in valid_options:
                    if response_lower == option.lower():
                        return option
                
                # If no exact match, show options
                self.display_text(f"Please enter one of: {', '.join(valid_options)}", "warning")
                
            except KeyboardInterrupt:
                self.display_text("\nGame interrupted by user.", "info")
                sys.exit(0)
            except EOFError:
                self.display_text("\nInput error occurred.", "error")
                continue
    
    def get_number_input(self, prompt: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> float:
        """Get numeric input with validation"""
        while True:
            try:
                response = input(prompt).strip()
                value = float(response)
                
                if min_val is not None and value < min_val:
                    self.display_text(f"Value must be at least {min_val}", "warning")
                    continue
                
                if max_val is not None and value > max_val:
                    self.display_text(f"Value must be no more than {max_val}", "warning")
                    continue
                
                return value
                
            except ValueError:
                self.display_text("Please enter a valid number.", "warning")
            except KeyboardInterrupt:
                self.display_text("\nGame interrupted by user.", "info")
                sys.exit(0)
    
    def display_menu(self, title: str, options: List[str]) -> str:
        """Display a menu and get user selection"""
        print()
        self.display_header(title)
        
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print()
        
        valid_choices = [str(i) for i in range(1, len(options) + 1)]
        choice = self.get_input(f"Choose an option (1-{len(options)}): ", valid_choices)
        
        return choice
    
    def display_financial_status(self, status: Dict[str, Any]):
        """Display formatted financial status"""
        print()
        self.display_header("FINANCIAL STATUS")
        
        # Basic info
        print(f"Age: {status.get('age', 'N/A')}")
        print(f"Month: {status.get('month', 'N/A')}")
        print()
        
        # Financial details
        cash = status.get('cash', 0)
        print(f"Cash: ${cash:,.2f}")
        
        income = status.get('monthly_income', 0)
        if income > 0:
            print(f"Monthly Income: ${income:,.2f}")
        
        debt = status.get('education_debt', 0)
        if debt > 0:
            self.display_text(f"Student Debt: ${debt:,.2f}", "warning")
        
        savings = status.get('savings_account', 0)
        if savings > 0:
            self.display_text(f"Savings: ${savings:,.2f}", "success")
        
        net_worth = status.get('net_worth', 0)
        color = "success" if net_worth >= 0 else "warning"
        self.display_text(f"Net Worth: ${net_worth:,.2f}", color)
        
        credit_score = status.get('credit_score', 650)
        if credit_score >= 750:
            credit_color = "success"
        elif credit_score >= 650:
            credit_color = "normal"
        else:
            credit_color = "warning"
        self.display_text(f"Credit Score: {credit_score}", credit_color)
        
        wellbeing = status.get('wellbeing_score', 50)
        if wellbeing >= 70:
            wellbeing_color = "success"
        elif wellbeing >= 40:
            wellbeing_color = "normal"
        else:
            wellbeing_color = "warning"
        self.display_text(f"Well-being: {wellbeing}/100", wellbeing_color)
        print()
    
    def display_progress_bar(self, current: int, total: int, label: str = ""):
        """Display a simple text progress bar"""
        if total <= 0:
            return
        
        percentage = (current / total) * 100
        bar_length = 30
        filled_length = int(bar_length * current / total)
        
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        
        if label:
            print(f"{label}: [{bar}] {percentage:.1f}% ({current}/{total})")
        else:
            print(f"[{bar}] {percentage:.1f}% ({current}/{total})")
    
    def clear_screen(self):
        """Clear the console screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pause_for_input(self, message: str = "Press Enter to continue..."):
        """Pause and wait for user input"""
        try:
            input(message)
        except KeyboardInterrupt:
            self.display_text("\nGame interrupted by user.", "info")
            sys.exit(0)
    
    def display_story_text(self, text: str, pause_after: bool = True):
        """Display story text with optional pause"""
        print()
        # Word wrap for better readability
        words = text.split()
        current_line = ""
        
        for word in words:
            if len(current_line + word) <= self.width - 2:
                current_line += word + " "
            else:
                if current_line:
                    print(current_line.strip())
                current_line = word + " "
        
        if current_line:
            print(current_line.strip())
        
        print()
        
        if pause_after:
            self.pause_for_input()
    
    def display_achievement(self, achievement_name: str, description: str):
        """Display an achievement notification"""
        print()
        self.display_text("🏆 ACHIEVEMENT UNLOCKED! 🏆", "success")
        self.display_text(f"   {achievement_name}", "bold")
        self.display_text(f"   {description}")
        print()


class GUIInterface(UserInterface):
    """Placeholder for future GUI implementation"""
    
    def __init__(self):
        # This will be implemented when we add GUI support
        # Could use tkinter, PyQt, or web-based interface
        raise NotImplementedError("GUI interface not yet implemented")
    
    def display_text(self, text: str, style: str = "normal"):
        raise NotImplementedError("GUI interface not yet implemented")
    
    def display_header(self, text: str):
        raise NotImplementedError("GUI interface not yet implemented")
    
    def display_separator(self, length: int = 50):
        raise NotImplementedError("GUI interface not yet implemented")
    
    def get_input(self, prompt: str, valid_options: Optional[List[str]] = None) -> str:
        raise NotImplementedError("GUI interface not yet implemented")
    
    def get_number_input(self, prompt: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> float:
        raise NotImplementedError("GUI interface not yet implemented")
    
    def display_menu(self, title: str, options: List[str]) -> str:
        raise NotImplementedError("GUI interface not yet implemented")
    
    def display_financial_status(self, status: Dict[str, Any]):
        raise NotImplementedError("GUI interface not yet implemented")
    
    def display_progress_bar(self, current: int, total: int, label: str = ""):
        raise NotImplementedError("GUI interface not yet implemented")
    
    def clear_screen(self):
        raise NotImplementedError("GUI interface not yet implemented")
    
    def pause_for_input(self, message: str = "Press Enter to continue..."):
        raise NotImplementedError("GUI interface not yet implemented")


def create_interface(interface_type: str = "console") -> UserInterface:
    """Factory function to create appropriate interface"""
    if interface_type.lower() == "console":
        return ConsoleInterface()
    elif interface_type.lower() == "gui":
        return GUIInterface()
    else:
        raise ValueError(f"Unknown interface type: {interface_type}")


if __name__ == "__main__":
    # Test the console interface
    ui = create_interface("console")
    
    ui.display_header("Interface Test")
    ui.display_text("This is normal text")
    ui.display_text("This is success text", "success")
    ui.display_text("This is warning text", "warning")
    ui.display_text("This is error text", "error")
    
    ui.display_progress_bar(7, 10, "Test Progress")
    
    # Test financial status display
    test_status = {
        'age': 18,
        'month': 3,
        'cash': 1250.50,
        'monthly_income': 2400.00,
        'education_debt': 15000.00,
        'savings_account': 500.00,
        'net_worth': -13249.50,
        'credit_score': 680,
        'wellbeing_score': 65
    }
    
    ui.display_financial_status(test_status)
    
    print("Interface test completed!")