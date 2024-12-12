import pytest
import monthly_budget as mb
import Visualization as vz 
import random


class TestExpenseTracker:
    
    """
    Unit tests for the ExpenseTracker class.
    """
    
    def test_monthly_expenses(self):
        
        """
        Tests the ExpenseTracker class making sure that expenses start at 0
        and the expense list matches the initialized categories.
        
        """
        
        # Create an instance of ExpenseTracker with a default user
        tracker = mb.ExpenseTracker(name="User")
        
        # Check if total expenses start at 0
        assert tracker.added_expenses() == 0 
        
        # Check if the expense list matches the initialized categories with all values set to 0
        assert tracker.list_expenses() == {"Housing": 0,"Groceries": 0,"Transportation": 0,"Entertainment": 0,"Healthcare": 0}
    
    def test_add_expenses(self):
        
        """
        Test the input of monthly expenses and verify the totals and category values update correctly.
        """
        
        # Create an instance of ExpenseTracker
        tracker = mb.ExpenseTracker(name="User ")
        
        
        # Add an expense to the 'Housing' category
        tracker.input_monthly_expenses("Housing", 1000)
        
        # checked if the 'Housing' expense is updated correctly
        
        assert tracker.list_expenses()["Housing"] == 1000
        
        # checked if  the total added expenses match the expected value
        assert tracker.added_expenses() == 1000
        
        # Add expenses to 'Groceries' and 'Transportation'
        tracker.input_monthly_expenses("Groceries", 200)
        tracker.input_monthly_expenses("Transportation", 150)
        
        # checked if updated expense list matches expected values
        assert tracker.list_expenses() == {"Housing": 1000, "Groceries": 200, "Transportation": 150, "Entertainment": 0, "Healthcare": 0}

class TestBudgetLimit:
    
    """
    Unit tests for the BudgetLimit class.
    """
    
    def test_set_budget(self):
    
        """
        Test setting a budget for a specific category and verifying total allocation updates.
        """
        
        budget = mb.BudgetLimit(total_budget=1000)
        budget.set_budget(300, "Housing")
        assert budget.budget_limit["Housing"] == 300
        assert budget.totalallocated == 300
    
    def test_adjustments(self):
        
        """
        Test budget adjustments when total allocation exceeds the threshold.
        """
        
        # Initialize the BudgetLimit instance with a total budget of 1000
        budget = mb.BudgetLimit(total_budget=1000)
        
        # Set an initial budget allocation of 600 for the 'Housing' category
        budget.set_budget(600, "Housing")
        
        # Set an initial budget allocation of 500 for the 'Groceries' category
        budget.set_budget(500, "Groceries")
        
        # Call the adjustments method to calculate adjustments for exceeding the threshold
        adjusted_amounts = budget.adjustments()
        
        # checks if adjustments is not none 
        assert adjusted_amounts is not None
        # Check if 'Housing' is included in the adjusted amounts
        assert "Housing" in adjusted_amounts
        
        # Check if 'Groceries' is included in the adjusted amounts
        assert "Groceries" in adjusted_amounts
        
        #Sum up all adjusted values and verify they do not exceed the threshold
        totaladjustment = sum(adjusted_amounts.values())
        
        # The assertion ensures that the total adjusted amounts remain within the limit 
        assert totaladjustment <= budget.total_budget * budget.threshold
    
    def test_update_budget_limits(self):
        
        """
        Test updating budget limits with adjusted values and verify consistency.
        """
        
        #Initialize the BudgetLimit instance with a total budget of 1000
        budget = mb.BudgetLimit(total_budget=1000)
        
        # initial allocation of 600 for the 'Housing' category
        budget.set_budget(600, "Housing")
        
        # Set an initial allocation of 500 for the 'Groceries' category
        
        budget.set_budget(500, "Groceries")
        
        
        #Generate adjusted budget amounts and update the limits
        adjusted_amount = budget.adjustments()
        budget.update_budget_limits(adjusted_amount)
        
        # checked the updated budget matches the adjusted values
        assert budget.budget_limit == adjusted_amount
        
        # checked the total allocated budget matches the adjusted values 
        assert budget.totalallocated == sum(adjusted_amount.values())
    
    def test_delete_category(self):

        """
        Test deleting a budget category and verifying updates to the total allocation.
        """

        # Create a BudgetLimit instance with a total budget of 1000
        budget = mb.BudgetLimit(total_budget=1000)
        
        #Set budget allocations for housing categorie
        budget.set_budget(200, "Housing")
        # Set budget allocations for grocery categories
        budget.set_budget(300, "Groceries")
        
        # Delete the 'Housing' category
        message = budget.delete_category("Housing")
        
        # checked if message removed housing
        assert message == "Removed budgeting for Housing"
        
        # checked if 'Housing' category was removed 
        assert "Housing" not in budget.budget_limit
        
        #checked if total allocated budget updated correctly 
        assert budget.totalallocated == 300
        
        # Delete the 'Transportation' category 
        message = budget.delete_category("Transportation")
        
        # checked if message says that the category doesn't exxist 
        assert message == "Category Transportation does not exist "
    
    def test_all_items(self):
        
        """
        Test retrieving all budget categories and their allocations.
        """
        
        #Initialize a BudgetLimit instance with a total budget of 1000
        budget = mb.BudgetLimit(total_budget=1000)
        
        # Set budget allocation of 200 for 'Housing'
        budget.set_budget(200, "Housing")
        
        #Set budget allocation of 300 for 'Groceries'
        budget.set_budget(300, "Groceries")

        # used all_items() to get all budget categories 
        all_items = budget.all_items()
        
        # check that all items match the dictionary of categories and allocations
        assert all_items == {"Housing": 200, "Groceries": 300}

class TestExpenseLog:
    
    """
    Unit tests for the ExpenseLog class.
    """
    
    def test_budget_random(self):
        
        """
        Test the random allocation of budgets and expenses for simulation.
        
        """
        #Initialize an ExpenseLog instance with a total budget of 5000 and a user name
        expenselog = mb.ExpenseLog(total_budget=5000, name = "User")
        
        # Randomly allocate budgets to different categories
        expenselog.budget_random(expenselog.budget_limit)
        
        # check that the randomly allocated total budget falls within the range 
        assert 4000 <= expenselog.budget_limit.total_budget <= 8000
        # used for loop to iterate over budgets 
        for budget in expenselog.budget_limit.all_items().values():
            assert 400 <= budget <= 1000 # checked if budgets are within the range 
            
        #  used for loop to iterate over expenses
        
        for expense in expenselog.expense_tracker.list_expenses().values():
            assert 100 <= expense <= 1400 # checked if expenses are within the range 
    
    def test_main(self):
        
        """
         Test the main function to verify initialization of ExpenseLog instances.
        
        """
        
        # Open the "names.txt" file to get a  list of names
        with open("names.txt", "r") as file:
            listofnames = file.read().split() # split names in the list 
            assert len(listofnames) > 0 # checked if the file has more than one name
        
        # made an empty list to store ExpenseLog instances
        expense_log_inst_list = []

        # used for loop to iterate over the list of names 
        for name in listofnames:
        # Create an ExpenseLog instance with a random total budget for each user
            expense_log_inst = mb.ExpenseLog(total_budget=random.randint(2000,10000),name=name)
        # Randomly allocate budgets to different categories for the current user
            expense_log_inst.budget_random(budget=expense_log_inst.budget_limit)

        # Append the ExpenseLog instance to the list
            expense_log_inst_list.append(expense_log_inst)        
            
        # checked the number of created ExpenseLog instances matches the number of names
        assert len(expense_log_inst_list) == len(listofnames)
        
        # used for loop to iterate over expense_log_inst_list 
        for expense_log in expense_log_inst_list:
        
        # checked if ExpenseLog total budget falls into range
            assert 2000 <= expense_log.budget_limit.total_budget <= 10000
        
        #used for loop to iterate over each budget category 
        for budget in expense_log.budget_limit.all_items().values():
            assert 400 <= budget <= 1000 # checked if budget category falls into range 
        
        # used for loop to iterate over expense value 
        for expense in expense_log.expense_tracker.list_expenses().values():
                assert 100 <= expense <= 1400 # checked if expense values falls into range

class TestPlots:
   
    """
    Unit tests for the Plots class.
    
    """

   
    def test_init(self):
        
        """
         Test initialization of the Plots class and the processing of data.
        """
        #Create a list of ExpenseLog instances with specific total budgets and user names
        expense_log_inst_list = [ mb.ExpenseLog(total_budget=5000, name="User1"),   
                                                mb.ExpenseLog(total_budget=7000, name="User2"),] 
        
        # used for loop to iterate over each item in expense_log_inst_list 
        for expense_log_inst in expense_log_inst_list:
        
        # used budget_random to randomly allocate budget and expenses 
            expense_log_inst.budget_random(expense_log_inst.budget_limit)
        
        # Create plots with list of ExpenseLog instances 
        plots = vz.Plots(expense_log_inst_list)
        
        # Check if the number of entries in the dataframe is  twice the number of ExpenseLog instances
        assert len(plots.budget_and_expenses_list_for_df) == len(expense_log_inst_list) * 2
        
        #check that the list of data for visualization is greater than zero
        assert len(plots.budget_and_expenses_list_for_viz) > 0
        
    
    def test_plot_creations(self):
        
        