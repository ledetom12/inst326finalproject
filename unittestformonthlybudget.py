import pytest
import monthly_budget as mb
import Visualization as vz 
import random


class TestExpenseTracker:
    
    def test_monthly_expenses(self):
        
        tracker = mb.ExpenseTracker(name="User")
        assert tracker.added_expenses() == 0 
        assert tracker.list_expenses() == {"Housing": 0,"Groceries": 0,"Transportation": 0,"Entertainment": 0,"Healthcare": 0}
    
    def test_add_expenses(self):
        
        tracker = mb.ExpenseTracker(name="User ")
        tracker.input_monthly_expenses("Housing", 1000)
        assert tracker.list_expenses()["Housing"] == 1000
        assert tracker.added_expenses() == 1000
        tracker.input_monthly_expenses("Groceries", 200)
        tracker.input_monthly_expenses("Transportation", 150)
        assert tracker.list_expenses() == {"Housing": 1000, "Groceries": 200, "Transportation": 150, "Entertainment": 0, "Healthcare": 0}

class TestBudgetLimit:
    
    def test_set_budget(self):
        budget = mb.BudgetLimit(total_budget=1000)
        budget.set_budget(300, "Housing")
        assert budget.budget_limit["Housing"] == 300
        assert budget.totalallocated == 300
    
    def test_adjustments(self):
        
        budget = mb.BudgetLimit(total_budget=1000)
        budget.set_budget(600, "Housing")
        budget.set_budget(500, "Groceries")
        adjusted_amounts = budget.adjustments()
        assert adjusted_amounts is not None
        assert "Housing" in adjusted_amounts
        assert "Groceries" in adjusted_amounts
        totaladjustment = sum(adjusted_amounts.values())
        assert totaladjustment <= budget.total_budget * budget.threshold
    
    def test_update_budget_limits(self):
        
        budget = mb.BudgetLimit(total_budget=1000)
        budget.set_budget(600, "Housing")
        budget.set_budget(500, "Groceries")

        adjusted_amount = budget.adjustments()
        budget.update_budget_limits(adjusted_amount)
        assert budget.budget_limit == adjusted_amount
        assert budget.totalallocated == sum(adjusted_amount.values())
    
    def test_delete_category(self):
        
        budget = mb.BudgetLimit(total_budget=1000)
        budget.set_budget(200, "Housing")
        budget.set_budget(300, "Groceries")
        message = budget.delete_category("Housing")
        assert message == "Removed budgeting for Housing"
        assert "Housing" not in budget.budget_limit
        assert budget.totalallocated == 300
        message = budget.delete_category("Transportation")
        assert message == "Category Transportation does not exist "
    
    def test_all_items(self):
        
        budget = mb.BudgetLimit(total_budget=1000)
        budget.set_budget(200, "Housing")
        budget.set_budget(300, "Groceries")

        all_items = budget.all_items()
        assert all_items == {"Housing": 200, "Groceries": 300}

class TestExpenseLog:
    def test_budget_random(self):
        expenselog = mb.ExpenseLog(total_budget=5000, name = "User")
        expenselog.budget_random(expenselog.budget_limit)
        assert 4000 <= expenselog.budget_limit.total_budget <= 8000
        for budget in expenselog.budget_limit.all_items().values():
            assert 400 <= budget <= 1000
            
        for expense in expenselog.expense_tracker.list_expenses().values():
            assert 100 <= expense <= 1400
    
    def test_main(self):
        with open("names.txt", "r") as file:
            listofnames = file.read().split()
            assert len(listofnames) > 0 
        
        expense_log_inst_list = []

        for name in listofnames:
            expense_log_inst = mb.ExpenseLog(total_budget=random.randint(2000,10000),name=name)
            expense_log_inst.budget_random(budget=expense_log_inst.budget_limit)

            expense_log_inst_list.append(expense_log_inst)        
            
    
        assert len(expense_log_inst_list) == len(listofnames)
        for expense_log in expense_log_inst_list:
            assert 2000 <= expense_log.budget_limit.total_budget <= 10000
        
        for budget in expense_log.budget_limit.all_items().values():
            assert 400 <= budget <= 1000
        
        for expense in expense_log.expense_tracker.list_expenses().values():
                assert 100 <= expense <= 1400

class TestPlots:
   
    def test_init(self):
        
        expense_log_inst_list = [ mb.ExpenseLog(total_budget=5000, name="User1"),
                                                mb.ExpenseLog(total_budget=7000, name="User2"),]
        for expense_log_inst in expense_log_inst_list:
            expense_log_inst.budget_random(expense_log_inst.budget_limit)
        
        plots = vz.Plots(expense_log_inst_list)
        assert len(plots.budget_and_expenses_list_for_df) == len(expense_log_inst_list) * 2
        assert len(plots.budget_and_expenses_list_for_viz) > 0
        
    
    def test_plot_creations(self):
        
        