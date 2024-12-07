import pandas as pd
import seaborn as sns

class Plots:
    def __init__(self,expense_log_inst_list):
        self.budget_and_expenses_list_for_df = []
        self.budget_and_expenses_list_for_viz = []
        for each_expense_inst in expense_log_inst_list:
            expense_tracker = each_expense_inst.expense_tracker
            budget_limit = each_expense_inst.budget_limit

            expense_dict_for_df = {"Name": each_expense_inst.expense_tracker.name, "Key": "Expense"}
            budget_dict_for_df = {"Name": each_expense_inst.expense_tracker.name, "Key": "Budget"}

            total_expenses = 0
            total_budget = 0
            for category,expenses in expense_tracker.list_expenses().items():
                expense_dict_for_viz = {"Key": "Expense", "Category": category, "Amount": expenses}
                self.budget_and_expenses_list_for_viz.append(expense_dict_for_viz)

                expense_dict_for_df[category] = expenses
                total_expenses += expenses
            expense_dict_for_df["Total"] = total_expenses
            self.budget_and_expenses_list_for_df.append(expense_dict_for_df)
                
            for category,budgeting in budget_limit.all_items().items():
                budget_dict_for_viz = {"Key": "Budget", "Category": category, "Amount": budgeting}
                self.budget_and_expenses_list_for_viz.append(budget_dict_for_viz)
               
                budget_dict_for_df[category] = budgeting
                total_budget += budgeting
            budget_dict_for_df["Total"] = total_budget
            self.budget_and_expenses_list_for_df.append(budget_dict_for_df)


    def plot_creations(self):
        expenses_and_budget_df = pd.DataFrame(self.budget_and_expenses_list_for_df)
        print(expenses_and_budget_df.to_string())

        
        expenses_and_budget_df.to_csv("Expenses and Budget.csv",index=False)
        
        expenses_and_budget_df_for_viz = pd.DataFrame(self.budget_and_expenses_list_for_viz)
       
        expenses_and_budget_plot = sns.barplot(data = expenses_and_budget_df_for_viz, x = "Category", y = "Amount", hue = "Key")
  
        expenses_and_budget_plot.get_figure().savefig("Expenses and Budget Visualization.png", format = "png")
