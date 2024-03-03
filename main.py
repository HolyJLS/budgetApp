import json
import os

class Budget:
    def __init__(self, income, target_savings):
        self.income = income 
        self.target_savings = target_savings
        self.categories = {}

    def add_category(self, name):
        self.categories[name] = 0

    def update_category_budget(self, name, amount):
        self.categories[name] = amount

    def show_budget(self):
        print("\nBudget Overview:")
        print(f"Income: ${self.income}")
        print(f"Target Savings: ${self.target_savings}")
        print("\ncategories:")
        for category, Budget in self.categories.items():
            print(f"{category}: ${Budget}")

    def remaining_budget(self, num_months):
        total_expenses = sum(self.categories.values()) * num_months 
        total_income = self.income * num_months
        return total_income - total_expenses
    
    def save_money(self, num_months):
        return self.income * num_months - self.remaining_budget(num_months)
    
def load_expenses_from_json(filename):
    if not os.path.exists(filename):
        print(f"ERROR: JSON file '{filename}' does not exist")
        return {}
    with open(filename, 'r') as file:
        try:
            expenses_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"ERROR: JSON decoding error: {e}")
            return {}
    return expenses_data.get('expenses', {}) 

def save_expenses_to_json(filename, expenses):
    with open(filename, 'w') as file:
        json.dump({"expenses": expenses}, file, indent=4)

def prompt_user_for_expenses(expenses):
    user_expenses = {}
    print("Please enter your expenses for each category:")
    for category, items in expenses.items():
        user_expenses[category] = {}
        print(f"\nCategory: {category}")
        for item, value in items.items():
            expense = float(input(f"Enter expense for '{item}': ${value} (current): "))
    return user_expenses




def main():
    income = float(input("Enter your monthly income: "))
    num_months = int(input("Enter the number of months you want to budget for: "))
    target_savings = float(input(f"Enter your target savings for the next {num_months} months: $"))

    my_budget = Budget(income, target_savings)
    
    expenses_file = 'common_expenses.json'
    expenses = load_expenses_from_json(expenses_file)
    if not expenses:
        print("No expenses data loaded. Exiting.")
        return
    
    print("Loaded expenses from JSON file:")
    print(expenses)

    """   for category in expenses:
        my_budget.add_category(category)"""

    user_expenses = prompt_user_for_expenses(expenses)

    for category, items in user_expenses.items():
        for item, value in items.items():
            expenses[category][item]= value

    my_budget.show_budget()

    remaining_budget = my_budget.remaining_budget(num_months)
    print(f"\nRemaining Budget: ${remaining_budget}")

    saved_money = my_budget.save_money(num_months)
    print(f"Money Saved for the next {num_months} months: ${saved_money}")


    if saved_money >= target_savings:
        print(f"Congrats! You have reached your savings target for the next {num_months} months")
    else:
        print(f"You are short of your savings target for the next {num_months} months. Consider adjusting your budget")

    save_expenses_to_json(expenses_file, expenses)

if __name__  == "__main__":
    main()




