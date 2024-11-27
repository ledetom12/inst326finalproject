import pytest 
import expense_tracker as exp

class TestExpenseTracker:
    def test_input_monthly_expenses(self):
        tracker = exp.ExpenseTracker("User")
        total = tracker.input_monthly_expenses("Groceries", 200)
        assert tracker.all_expenses["Groceries"] == 200
        assert total == 200

class TestBudgetLimit:
    def test_set_budget(self):
        budget = exp.BudgetLimit(total_budget=4000, threshold= 0.8)
        budget.set_budget(1500, "Housing")
        assert budget.budget_limit["Housing"] == 1500
        assert budget.totalallocated == 1500
    def test_adjustments(self):
        budget = exp.BudgetLimit(total_budget=4000, threshold= 0.8)
        budget.set_budget(2000, "Housing")
        expected_ratio = 3200/4000
        adjustments = budget.adjustments()
        
        assert adjustments is None
        assert adjustments["Housing"] == int(2000 * expected_ratio *100) /100