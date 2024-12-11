import Visualization as vz
import random
import pandas as pd
import seaborn as sns



class ExpenseTracker:
    
    """
    Tracks and manages monthly expenses for a user across various categories
    
    Attributes:
    all_expenses(dict): Dictionary to store expenses for categories 
    name(str): name of user 
    """
    def __init__(self,name):
       
        """
        Initializes the ExpenseTracker class with a user's name and a dictionary of expenses 
        
        Parameters:
        name(str): name of user
        
        """
        
        self.all_expenses = {"Housing": 0,"Groceries": 0,"Transportation": 0,"Entertainment": 0,"Healthcare": 0}
        self.name = name

    def input_monthly_expenses(self,expense,amount_for_expense):
        
        """
        Updates the expense amount for a specific category 
        
        Parameters:
        expense(str): the category of expense
        amount_for_expense(float): the amount spent in the category to be added
        
        """
        
        
        if expense in self.all_expenses:
            self.all_expenses[expense] += amount_for_expense


    def added_expenses(self):  
        
        """
        calculates the total monthly expenses across all categories 
        
        returns:
        
        float: the total of all expenses 
        
        """
        
        total_expenses = 0
        for each_expense in self.all_expenses.values():
            total_expenses += each_expense
        return total_expenses
    
    def list_expenses(self):
        
        """
        provides a summary of all expenses in each category

        Returns:
        
        dict: dictionary with categories as keys and their expense amounts as values
        
        """
        
        return self.all_expenses


class BudgetLimit:
    
    """the class defines the budget based on the user's total income
    and distributes amongst categories.
    
    Attributes:
    
    threshold(float): a decimal representing maximum allowed portion of total income 
    totalallocated(float): tracks the total amount of money allocated across all categories 
    budget_limit(dict): a dictionary that stores the budget limit for each category
    total_budget(float): the budget limit for the month, depending on the income of the user.
    """

    def __init__(self, total_budget):
        
        """
        initializes the BudgetLimit class with the total budget
        
        Parameters:
        total_budget(float): total amount of money available for 
        budgeting 
        """
        
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
        
        Raises:
        
        ValueError: if the total allocation exceeds the user's total budget
        """
        maximum_allowed = self.total_budget * self.threshold
 
        if maximum_allowed > self.total_budget:
            raise ValueError("Budget allocation exceeds total budget!")
        
        
        self.totalallocated -= self.budget_limit.get(category, 0)
        self.budget_limit[category] = money_amount
        self.totalallocated += money_amount
    
    def adjustments(self):
        
        """
        adjusts budget allocation, if the total allocated amount exceeds the 
        allowed limit
        
        Returns:
        dict: a dictionary with reduced allocations for each category 
        
        """
        maximum_allowed = self.total_budget * self.threshold
        if self.totalallocated <= maximum_allowed:
            return None
        reductionratio = maximum_allowed / self.totalallocated
        adjusted_amount = {}
        for category, amount in self.budget_limit.items():
            adjusted_amount[category] = int(amount* reductionratio *100)/100
        return adjusted_amount
    
    def update_budget_limits(self, adjusted_amount):
        
        """
        updates the current budget limits with new adjusted value and recalculates
        the total
        
        Parameters:
        adjusted_amount(dict): dictionary of adjusted budget amounts for each category 
        
        """
        
        self.budget_limit = adjusted_amount
        self.totalallocated = 0
        for value in adjusted_amount.values():
            self.totalallocated += value 
    
    def delete_category(self, category):
        
        """
        removes a specific category from the budget and adjusts the total
        allocated budget 
        
        Parameters:
        category(str): the category to be removed from the budget.
        

        Returns:
        str: a message indicating whether the category was successfully
        removed or does not exist
            
        """
        
        if category in self.budget_limit:
            self.totalallocated -= self.budget_limit.pop(category)
            return f"Removed budgeting for {category}"
        else:
            return f"Category {category} does not exist "

    def all_items(self):
        
        """
        gets current state of all budget allocations

        Returns:

        dict: a dictionary containing all budget categories and their
        allocated amounts 
        """
        
        return self.budget_limit


class ExpenseLog:
    
    """
    the class manages an expense log combining expenses
    and budget limits for a user
    
    attributes:
    expense_tracker: an instance of the ExpenseTracker class
    budget_limit: an instance of the BudgetLimit class
    """
    
    def __init__(self,total_budget,name):
        
        """
        initializes the ExpenseLog instance with a user's name
        and total budget.
        """
        self.expense_tracker = ExpenseTracker(name)
        self.budget_limit = BudgetLimit(total_budget)


    def budget_random(self, budget):
        
        """
        randomly assigns a new total budget and allocates 
        random budgets and expenses to specific categories for simulation 

        Parameters:
        
        budget: users budget instance 
        
        """
        
        income = random.randint(4000,8000)
        budget.total_budget = income
        

        for category in self.expense_tracker.list_expenses().keys():
            try: 
                randombudget = random.randint(400,1000)
                self.budget_limit.set_budget(randombudget, category)
            except ValueError:
                print("value does not work")
        
        for category in self.expense_tracker.list_expenses().keys():
            randomexpense = random.randint(100, 1400)
            self.expense_tracker.input_monthly_expenses(category, randomexpense)
        
            
def main():
    
    """
    initializes the ExpenseLog instances for multiple users and generates plot from 
    from Vizualization file
    """
    
    with open("Names.txt",'r') as file:
        all_names = file.read()
        list_of_names = all_names.split()
    
    expense_log_inst_list = []

    for name in list_of_names:
        expense_log_inst = ExpenseLog(total_budget=random.randint(2000,10000),name=name)
        expense_log_inst.budget_random(budget=expense_log_inst.budget_limit)

        expense_log_inst_list.append(expense_log_inst)

    plots_inst = vz.Plots(expense_log_inst_list)

    plots_inst.plot_creations()

if __name__ == "__main__":
    main()
    

