class expense_tracker():
    """
    Obtains information of expenses inputed from user in order to keep track of monthly
    expenses.
    """
    def __init__(housing_exp=0.0,internet_exp=0.0,entertainment_exp=0.0,groceries_exp=0.0,transportation_exp=0.0):
        """
        Initializes starting point as 0 for expenses. Makes sure we recieve an integer
        """