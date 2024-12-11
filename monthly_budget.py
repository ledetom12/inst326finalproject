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
        
        #initializes the expense dictionary with the default value of zero
        self.all_expenses = {"Housing": 0,"Groceries": 0,"Transportation": 0,"Entertainment": 0,"Healthcare": 0}
        
        # name of user 
        self.name = name

    def input_monthly_expenses(self,expense,amount_for_expense):
        
        """
        Updates the expense amount for a specific category 
        
        Parameters:
        expense(str): the category of expense
        amount_for_expense(float): the amount spent in the category to be added
        
        """
        
        
        # checks if the expense category exists in dictionary and update its value
        if expense in self.all_expenses:
            self.all_expenses[expense] += amount_for_expense


    def added_expenses(self):  
        
        """
        calculates the total monthly expenses across all categories 
        
        returns:
        
        float: the total of all expenses 
        
        """
        
        # counter for total_expenses variable
        total_expenses = 0
        
        # for loop to iterate over all expense values and adds them to total
        for each_expense in self.all_expenses.values():
        
        # Adds the current expense amount to the running total of all expenses.
            total_expenses += each_expense
        
        # Returns the calculated total of all expenses
        return total_expenses
    
    def list_expenses(self):
        
        """
        provides a summary of all expenses in each category

        Returns:
        
        dict: dictionary with categories as keys and their expense amounts as values
        
        """
        
        return self.all_expenses # returns dictionary of expenses 


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
        
        self.total_budget = total_budget # sets total budget for user
        self.threshold = 0.8 # # sets threshold of budget
        self.budget_limit = {} # empty dictionary for budget limit per category 
        self.totalallocated = 0.0 # total amount allocated
    
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
        
        # calculates the maximum allowed budget based on threshold
        maximum_allowed = self.total_budget * self.threshold 
       
        # checks if the allocated amount does not exceed the allowed budget 
        if maximum_allowed > self.total_budget:
            raise ValueError("Budget allocation exceeds total budget!")
        
        #  adjusts the total allocation by removing old amount for category 
        self.totalallocated -= self.budget_limit.get(category, 0)
        
        # sets the new budget for the category
        self.budget_limit[category] = money_amount
        
        # adds new allocation to the total allocated amount 
        self.totalallocated += money_amount
    
    def adjustments(self):
        
        """
        adjusts budget allocation, if the total allocated amount exceeds the 
        allowed limit
        
        Returns:
        None: returns None if the total allocation is within limit
        dict: a dictionary with reduced allocations for each category 
        
        """
        
        # calculates the maximum allowed allocation 
        maximum_allowed = self.total_budget * self.threshold
        
        # returns None if the total allocation is within limit
        if self.totalallocated <= maximum_allowed:
            return None
        
        # calculates reduction ratio to adjust allocations
        reductionratio = maximum_allowed / self.totalallocated
        adjusted_amount = {}
        
        # uses for loop to adjust each categorys allocation using reduction ratio
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
        
        # replaces budjet limits with the adjusted values 
        self.budget_limit = adjusted_amount
        
        # resets total allocated amount to zero 
        self.totalallocated = 0
        
        # for loop to iterate through all values in adjusted_amount dictionary
        for value in adjusted_amount.values():
        
        # adds each adjusted amount to total of allocated budget
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

        # checks if category exists and removes it
        if category in self.budget_limit:
        
        # rmemoves the budget for the specificed category and subtract its amount 
            self.totalallocated -= self.budget_limit.pop(category)
            
        # returns a message if a category was removed 
            return f"Removed budgeting for {category}"
        else:
        
        # returns a message if a category does not exists 
            return f"Category {category} does not exist "

    def all_items(self):
        
        """
        gets current state of all budget allocations

        Returns:

        dict: a dictionary containing all budget categories and their
        allocated amounts 
        """
        
        # returns the budget_limit dictionary
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
        
        # initializes an ExpenseTracker for the user
        self.expense_tracker = ExpenseTracker(name)
        
        # initializes a BudgetLimit for the user
        self.budget_limit = BudgetLimit(total_budget)


    def budget_random(self, budget):
        
        """
        randomly assigns a new total budget and allocates 
        random budgets and expenses to specific categories for simulation 

        Parameters:
        
        budget: users budget instance 
        
        """
        
        # generates random using randint between 4000 and 8000
        income = random.randint(4000,8000)
        budget.total_budget = income
        
        # uses for loop to randomly set budgets for categories
        for category in self.expense_tracker.list_expenses().keys():
            try: 
            
            # assigns a random budget between 400 and 1000 to each category 
                randombudget = random.randint(400,1000)
                self.budget_limit.set_budget(randombudget, category)
            
            # ValueError message if the budget exceeds the allowed amount
            except ValueError:
                print("value does not work")
        
        # uses for loop to iterate through all expense categories 
        for category in self.expense_tracker.list_expenses().keys():
            
            # adds a random expense between 100 and 1400 to each category 
            randomexpense = random.randint(100, 1400)
        
        # Adds a randomly generated expense to the specified category in the ExpenseTracker instance.
            self.expense_tracker.input_monthly_expenses(category, randomexpense)
        
            
def main():
    
    """
    initializes the ExpenseLog instances for multiple users and generates plot from 
    from Vizualization file
    """
    
    # Opens the file "names.txt" in read mode to retrieve user names.
    
    with open("names.txt",'r') as file:
    
    # Reads the content of the file
        all_names = file.read()
    
    #Splits into a list of names
        list_of_names = all_names.split()
    
    # empty list to store ExpenseLog instances for each user
    expense_log_inst_list = []

    # for loop to iterate over list of names 
    
    for name in list_of_names:
    # Creates a new ExpenseLog instance with a random total budget and the user's name
        expense_log_inst = ExpenseLog(total_budget=random.randint(2000,10000),name=name)
    
        #Simulates random budget allocations and expenses for the user
        expense_log_inst.budget_random(budget=expense_log_inst.budget_limit)
        
        # Appends the created ExpenseLog instance to the list
        expense_log_inst_list.append(expense_log_inst)
    
    # Creates a Plots instance using the list of ExpenseLog instances for visualization
    plots_inst = vz.Plots(expense_log_inst_list)

    # Calls plot_creations to generate and display the plots
    plots_inst.plot_creations()

if __name__ == "__main__":
    
    main() # calls main function 
    

