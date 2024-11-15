class expense_tracker():
    """
    Obtains information of expenses inputed from user in order to keep track of monthly
    expenses.
    """
    def __init__(housing_exp=0.0,internet_exp=0.0,entertainment_exp=0.0,groceries_exp=0.0,transportation_exp=0.0):
        """
        Initializes starting point as 0 for expenses. Makes sure we recieve an integer
        """

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
        