import pandas as pd
import seaborn as sns

class Plots:
    
    """
    a class to generate vizualizations and summaries for budget and
    expenses
    
    Attributes:
    budget_and_expenses_list_for_df(list): list of dictionaries used to create dataframes
    budget_and_expenses_list_for_vz(list) list of dictionaries used to create vizualizations
    
    """
    
    def __init__(self,expense_log_inst_list):
        
        """
        Initializes plot class by processing list of Expense Log instances
        for vizualizations and summaries
        
        Parameters:
        expense_log_inst_list(list): list of Expense log instances containing budget and
        expenses
        
        """
        
        # initializes the list for creating dataframes 
        self.budget_and_expenses_list_for_df = []
        # initializes the list for creating visualizations 
        self.budget_and_expenses_list_for_viz = []
        self.expenses_and_budget_df = None
        self.expenses_and_budget_df_for_viz = None
        
        # for loop to iterate through each ExpenseLog instance
        for each_expense_inst in expense_log_inst_list:
        
        # gets ExpenseTracker instance from the current ExpenseLog
            expense_tracker = each_expense_inst.expense_tracker
        # Retrieves the BudgetLimit instance from the current ExpenseLog
            budget_limit = each_expense_inst.budget_limit
        
        # Initializes dictionaries to store data for expenses and budgets.
            expense_dict_for_df = {"Name": each_expense_inst.expense_tracker.name, "Key": "Expense"}
            budget_dict_for_df = {"Name": each_expense_inst.expense_tracker.name, "Key": "Budget"}

            total_expenses = 0 # counter for expenses
            total_budget = 0 # counter for budgets 
            
            # for loop to iterate through expense category to add data for visualization and summaries 
            for category,expenses in expense_tracker.list_expenses().items():
            
            # Creates a dictionary for visualizing this category's expense.
                expense_dict_for_viz = {"Key": "Expense", "Category": category, "Amount": expenses}
            
            # Appends the visualization dictionary to the list for visualizations
                self.budget_and_expenses_list_for_viz.append(expense_dict_for_viz)
            
            # Adds the expense to the dataframe dictionary
                expense_dict_for_df[category] = expenses
            
            # adds expenses together
                total_expenses += expenses
            
            # adds total expenses to dataframe dictionary
            expense_dict_for_df["Total"] = total_expenses
            
            # appends the expense dictionary to the list of dataframes 
            self.budget_and_expenses_list_for_df.append(expense_dict_for_df)
            
            # uses for loop to iterate through each budget category to add data for visualizations and summaries 
            
            for category, budgeting in budget_limit.all_items().items():
            # creates dictionary for visualizing categories budget
                budget_dict_for_viz = {"Key": "Budget", "Category": category, "Amount": budgeting}
            
            # Appends the visualization dictionary to the list for visualizations.
                self.budget_and_expenses_list_for_viz.append(budget_dict_for_viz)
              
            # Adds the budget to the dataframe dictionary.
                budget_dict_for_df[category] = budgeting
                
                total_budget += budgeting # adds more to the total budget
                

            budget_dict_for_df["Total"] = total_budget # adds total budget to dataframe dictioanry
            
            # appends budget dictionary to the list of dataframes 
            self.budget_and_expenses_list_for_df.append(budget_dict_for_df)


    def plot_creations(self):
        
        """
        creates a summary table and bar graphs vizualizing budgets and expenses
        
        """
        
        # converts the budget and expenses data into a dataframe
        self.expenses_and_budget_df = pd.DataFrame(self.budget_and_expenses_list_for_df)
        
        # prints the dataframe 
        print(self.expenses_and_budget_df.to_string())

        # saves dataframe into a csv file 
        self.expenses_and_budget_df.to_csv("Expenses and Budget.csv",index=False) 
        
        # converts visualization into a dataframe for plotting
        self.expenses_and_budget_df_for_viz = pd.DataFrame(self.budget_and_expenses_list_for_viz)
        
        # Creates a bar plot showing budgets and expenses by category, grouped by "Key".
        expenses_and_budget_plot = sns.barplot(data = self.expenses_and_budget_df_for_viz, x = "Category", y = "Amount", hue = "Key")
        
        # Saves the generated bar plot as a PNG file.
        expenses_and_budget_plot.get_figure().savefig("Expenses and Budget Visualization.png", format = "png")
