import json
import shutil
import os

class Budget:
    def __init__(self, expenses):
        self.expenses = expenses

    def load_expenses_from_json(self, filename):
        if not os.path.exists(filename):
            print(f"ERROR: JSON file '{filename}' not found.")
            return {}
        with open(filename, 'r') as file:
            try:
                expenses_data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"ERROR: JSON decoding error: {e}")
                return {}
        self.expenses = expenses_data.get('expenses', {})

    def save_expenses_to_json(self, filename):
        with open(filename, 'w') as file:
            json.dump({"expenses": self.expenses}, file, indent=4)

    def prompt_user_for_expenses(self):
        user_expenses = {}
        print("Please enter your expenses for each category:")
        for category, items in self.expenses.items():
            user_expenses[category] = {}
            print(f"\nCategory: {category}")
            for item, value in items.items():
                expense = float(input(f"Enter expense for '{item}': ${value} (current): "))
                user_expenses[category][item] = expense

        for category, items in user_expenses.items():
            self.expenses.setdefault(category, {}).update(items)
        return user_expenses

def calculate_savings(monthly_income, expenses, budget_months):
    total_expenses = sum(sum(category.values()) for category in expenses.values()) * budget_months
    savings = monthly_income * budget_months - total_expenses
    return savings

def main():
    user_name = input("Enter your name: ")
    monthly_income = float(input("Enter your monthly income: $"))
    budget_months = int(input("Enter the number of months you want to budget for: "))

    common_expenses_file = 'common_expenses.json'
    user_expenses_file = f"{user_name}.json"
    shutil.copy(common_expenses_file, user_expenses_file)

    expenses = {}
    budget = Budget(expenses)

    budget.load_expenses_from_json(user_expenses_file)
    print(f"Loaded expenses from '{user_expenses_file}'")

    user_expenses = budget.prompt_user_for_expenses()

    savings = calculate_savings(monthly_income, budget.expenses, budget_months)

    budget.save_expenses_to_json(user_expenses_file)

    print(f"\nAfter budgeting for {budget_months} months, your savings will be: ${savings}")

if __name__ == "__main__":
    main()
