import pytest
import testing as t


class TestExpenseTracker:
    def test_monthly_expenses(self):
        tracker = t.ExpenseTracker(name="User")
        assert tracker.added_expenses() == 0 
        assert tracker.list_expenses() == {"Housing": 0,"Groceries": 0,"Transportation": 0,"Entertainment": 0,"Healthcare": 0}
    
    def test_add_expenses(self):
        
        tracker = t.ExpenseTracker(name="User ")
        tracker.input_monthly_expenses("Housing", 1000)
        assert tracker.list_expenses()["Housing"] == 1000
        assert tracker.added_expenses() == 1000
        tracker.input_monthly_expenses("Groceries", 200)
        tracker.input_monthly_expenses("Transportation", 150)
        assert tracker.list_expenses() == {"Housing": 1000, "Groceries": 200, "Transportation": 150, "Entertainment": 0, "Healthcare": 0}

class TestBudgetLimit:
    def test_set_budget(self):
        budget = t.BudgetLimit(total_budget=1000)
        budget.set_budget(300, "Housing")
        assert budget.budget_limit["Housing"] == 300
        assert budget.totalallocated == 300
    
    def test_adjustments(self):
        budget = t.BudgetLimit(total_budget=1000)
        budget.set_budget(600, "Housing")
        budget.set_budget(500, "Groceries")
        adjusted_amounts = budget.adjustments()
        assert adjusted_amounts is not None
        assert "Housing" in adjusted_amounts
        assert "Groceries" in adjusted_amounts
        totaladjustment = sum(adjusted_amounts.values())
        assert totaladjustment <= budget.total_budget * budget.threshold
    
    def test_update_budget_limits(self):
        budget = t.BudgetLimit(total_budget=1000)
        budget.set_budget(600, "Housing")
        budget.set_budget(500, "Groceries")

        adjusted_amount = budget.adjustments()
        budget.update_budget_limits(adjusted_amount)
        assert budget.budget_limit == adjusted_amount
        assert budget.totalallocated == sum(adjusted_amount.values())
    
    def test_delete_category(self):
        budget = t.BudgetLimit(total_budget=1000)
        budget.set_budget(200, "Housing")
        budget.set_budget(300, "Groceries")
        message = budget.delete_category("Housing")
        assert message == "Removed budgeting for Housing"
        assert "Housing" not in budget.budget_limit
        assert budget.totalallocated == 300
        message = budget.delete_category("Transportation")
        assert message == "Category does not exist"
    
    def test_all_items(self):
        budget = t.BudgetLimit(total_budget=1000)
        budget.set_budget(200, "Housing")
        budget.set_budget(300, "Groceries")

        all_items = budget.all_items()
        assert all_items == {"Housing": 200, "Groceries": 300}

class TestExpenseLog:
    def test_budget_random(self):
        expenselog = t.ExpenseLog(total_budget=5000, name = "User")
        expenselog.budget_random(expenselog.budget_limit)
        assert 4000 <= expenselog.budget_limit.total_budget <= 8000
        for budget in expenselog.budget_limit.all_items().values():
            assert 400 <= budget <= 1000
            
        for expense in expenselog.expense_tracker.list_expenses().values():
            assert 100 <= expense <= 1400