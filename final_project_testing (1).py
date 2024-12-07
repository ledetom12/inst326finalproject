from argparse import ArgumentParser
import random
import seaborn as sea 
import pandas as pd

class ExpenseTracker:
    """
    Obtains information of expenses inputed from user in order to keep track of monthly
    expenses.
    """
    def __init__(self,name):
        self.all_expenses = {"Housing": 0,"Groceries": 0,"Transportation": 0,"Entertainment": 0,"Healthcare": 0}
        self.name = name

    def input_monthly_expenses(self,expense,amount_for_expense):
        if expense in self.all_expenses:
            self.all_expenses[expense] += amount_for_expense


    ### made this into a function so it can be accessed later as a class object ####
    def added_expenses(self):
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

    def __init__(self, total_budget):
        
        self.total_budget = total_budget
        self.threshold = 0.8
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

        ###        changed so maximum isnt greater than budget and budget can be anything inputed   ###
        if maximum_allowed > self.total_budget:
            raise ValueError("Budget allocation exceeds total budget!")
        
        
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
            return f"Removed  budgeting for {category}"
        else:
            return f"Category {category} does not exist "

    def all_items(self):
        
        return self.budget_limit


 ### changed expense log so it can show everything when printed. it will show the amount per category for budget and expenses ####
 
class ExpenseLog:
    
    def __init__(self,total_budget,name):
        self.expense_tracker = ExpenseTracker(name)
        self.budget_limit = BudgetLimit(total_budget)

    def expense_per_category(self):
        all_expenses = self.expense_tracker.added_expenses()
        print("\nExpense Per Category:")
        for category,expense_amount in self.expense_tracker.list_expenses().items():
            print(f"{category}: ${expense_amount}")
        print(f"Total expenses = ${all_expenses}")
        

    def budget_per_category(self):
        total_budgeted = 0
        for budgeted_item in self.budget_limit.all_items().values():
            total_budgeted += budgeted_item
        print("\nBudget Per Category:")
        for category,budget_amount in self.budget_limit.all_items().items():
            print(f"{category}: ${budget_amount}")
        print (f"Adjusted Budget Per Category Total = ${total_budgeted}")
        
    def budget_random(self, budget):
        
        income = random.randint(4000,8000)
        budget.total_budget = income
        print(f"Randomly generated total income: ${income}")

        for category in self.expense_tracker.list_expenses().keys():
            try: 
                randombudget = random.randint(400,1000)
                self.budget_limit.set_budget(randombudget, category)
            except ValueError:
                print("value does not work")
        
        for category in self.expense_tracker.list_expenses().keys():
            randomexpense = random.randint(100, 1400)
            self.expense_tracker.input_monthly_expenses(category, randomexpense)
        print("random expenses: complete")
            
def dataframe(expense_log):
    expenses = expense_log.expense_tracker.list_expenses()
    budgets = expense_log.budget_limit.all_items()
    categories = list(expenses.keys())
    expensevalue = [expenses[cat] for cat in categories]
    budgetvalue = [budgets.get(cat, 0) for cat in categories]
    
    
    df = pd.DataFrame({
    "Category": categories,
    "Expenses" : expensevalue,
    "Budgets" : budgetvalue
    })

    return df

def main():
    with open("names.csv",'r') as file:
        all_names = file.read()
        list_of_names = all_names.split()
    
    for name in list_of_names:
        print(f"\nThese are the budgets and expenses for {name}\n")
    
        expense_log_inst = ExpenseLog(total_budget=random.randint(2000,10000),name=name)
        expense_log_inst.budget_random(budget=expense_log_inst.budget_limit)

        expense_log_inst.budget_per_category()

        expense_log_inst.expense_per_category()
        
        df = dataframe(expense_log_inst)
        print(df)


if __name__ == "__main__":
    main()
    

