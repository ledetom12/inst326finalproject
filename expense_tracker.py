
import random

class ExpenseTracker:
    """
    Obtains information of expenses inputed from user in order to keep track of monthly
    expenses.
    """
    def __init__(self,name):
        self.all_expenses = {}
        self.name = name

    def input_monthly_expenses(self,expense,amount_for_expense):
        if expense not in self.all_expenses:
            self.all_expenses[expense] = amount_for_expense
        elif expense in self.all_expenses:
            self.all_expenses[expense] += amount_for_expense

        total_expenses = 0
        for each_expense in self.all_expenses.values():
            total_expenses += each_expense
        return total_expenses
    
    def list_expenses(self):
        
        return self.all_expenses


class BudgetLimit:
    
    """the class defines the budget based on the user's total income
    and distributes amongst categories.
    
    Attributes:
    
    income(float): the monthly income of the user 
    budget_limit(dict): a dictionary that stores the budget limit for each category
    total_budget(float): the budget limit for the month, depending on the income
    """

    def __init__(self, total_budget=4000, threshold = 0.8):
        
        self.total_budget = total_budget
        self.threshold = threshold
        self.budget_limit = {}
        self.totalallocated = 0.0
    
    def set_budget(self, money_amount, category):
        """
        creates a budget limit for users in a specific category and checks 
        how much they have left
        
        parameters:
        category(str):  the category that the budget limit is set too
        money_amount(float): the amount that is spent in the category
        
        """
        maximum_allowed = self.total_budget * self.threshold
        if self.totalallocated - self.budget_limit.get(category, 0) + money_amount > maximum_allowed:
            raise ValueError("Budget allocation exceeds total budget of 4000!")
        
        
        self.totalallocated -= self.budget_limit.get(category, 0)
        self.budget_limit[category] = money_amount
        self.totalallocated += money_amount
    
    def adjustments(self):
        maximum_allowed = self.total_budget * self.threshold
        if self.totalallocated <= maximum_allowed:
            return None
        reductionratio = maximum_allowed / self.totalallocated
        adjusted_amount = {}
        for category, amount in self.budget_limit.items():
            adjusted_amount[category] = int(amount* reductionratio *100)/100
        return adjusted_amount
    
    def update_budget_limits(self, adjusted_amount):
        
        self.budget_limit = adjusted_amount
        self.totalallocated = 0
        for value in adjusted_amount.values():
            self.totalallocated += value 
    
    def delete_category(self, category):
        
        if category in self.budget_limit:
            self.totalallocated -= self.budget_limit.pop(category)
            return f"Removed  budget for {category}"
        else:
            return f"Category {category} does not exist "

    def all_items(self):
        
        return self.budget_limit

class ExpenseLog:
    
    def __init__(self, name):
        self.allexpense = {}
        self.name = name
    
def budget_random(expenses, budget):
        
    categories = ["Housing", "Groceries", "Transportation","Entertainment","Healthcare"]
    income = random.randint(4000,8000)
    budget.total_budget = income
    print(f"Randomly generated total income: ${income}")
        
    for category in categories:
        try: 
            randombudget = random.randint(400,1000)
            budget.set_budget(randombudget, category)
        except ValueError:
            print("value does not work")
        
    for category in categories:
        randomexpense = random.randint(100, 1400)
        expenses.input_monthly_expenses(category, randomexpense)
        print("random expenses: complete")
            
def main(sequences=True):

    expensetracker = ExpenseTracker("User")
    budgetlimit = BudgetLimit()
    
    if sequences:
        budget_random(expensetracker, budgetlimit)
    
    expenselog = ExpenseLog(expensetracker, budgetlimit)
    expenselog

if __name__ == "__main__":