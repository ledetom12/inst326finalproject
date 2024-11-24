class ExpenseTracker():
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



class BudgetLimit:
    
    """the class defines the budget based on the user's total income
    and distributes amongst categories.
    
    Attributes:
    
    income(float): the monthly income of the user 
    budget_limit(dict): a dictionary that stores the budget limit for each category
    total_budget(float): the budget limit for the month, depending on the income
    """

    def __init__(self, income):
        
        self.income = income
        self.budget_limit = {}
        self.totalbudget = 0.0
    
    def set_budget(self, money_amount, category):
        """
        creates a budget limit for users in a specific category and checks 
        how much they have left
        
        parameters:
        category(str):  the category that the budget limit is set too
        money_amount(float): the amount that is spent in the category
    
    
        """
        
        self.budget_limit[category] = money_amount
        self.totalbudget += money_amount

"""
Unit tests for budget limit:

Tests when a false is put in below
200,0,3500.56,False,34

Tests what code does when string is added
200,"Tomato",45.56,90000,75.65

Tests when everything is correct
23.47,900.89,245,642,925

Make sure code knows what to do when false
298,87,0,0,0

Sees what code does when their is less inputs than required
358.09,78
"""
        